from typing import Dict, Union, Iterable, Set
from types import MappingProxyType  # Readonly dict

# docker_registry_client doesn't provide typing
# so we need to ignore it
from docker_registry_client import BaseClient  # type: ignore


class Base:
    def __init__(self, name: str):
        self.__name: str = name

    @property
    def name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return '{}({})'.format(type(self).__name__, self.name)


class Manifest(Base):
    def __init__(self,
                 client: BaseClient,
                 repo: str,
                 digest: str,
                 content: Union[Dict, None] = None):
        super().__init__('{}:{}'.format(repo, digest))
        self._client: BaseClient = client
        self._repo: str = repo
        self._digest: str = digest
        self._content: Union[Dict, None] = content

    @property
    def repository(self) -> str:
        return self._repo

    @property
    def content(self) -> MappingProxyType:
        if self._content is None:
            self._content, _ = self._client.get_manifest_and_digest(
                self._repo, self._digest)
        return MappingProxyType(self._content)

    @property
    def digest(self) -> str:
        return self._digest

    def delete(self) -> None:
        self._client.delete_manifest(self._repo, self._digest)


class Tag(Base):
    def __init__(self, client: BaseClient, repo: str, tag: str):
        super().__init__('{}:{}'.format(repo, tag))
        self._client: BaseClient = client
        self._repo: str = repo
        self._tag: str = tag
        self._manifest: Union[Manifest, None] = None

    @property
    def repository(self) -> str:
        return self._repo

    @property
    def tag(self) -> str:
        return self._tag

    @property
    def manifest(self) -> Manifest:
        if self._manifest is None:
            manifest, digest = self._client.get_manifest_and_digest(
                self._repo, self._tag)
            self._manifest = Manifest(self._client,
                                      self._repo,
                                      digest,
                                      manifest)
        return self._manifest

    def delete(self) -> None:
        self.manifest.delete()

    def __eq__(self, other) -> bool:
        return self._tag == other._tag and self._repo == other._repo


class Repository(Base):
    def __init__(self, client: BaseClient, repo: str):
        super().__init__(repo)
        self._client: BaseClient = client
        self._repo: str = repo
        self.__tags: Union[Dict[str, Tag], None] = None

    @property
    def _tags(self) -> Dict[str, Tag]:
        if self.__tags is None:
            self.__tags = {
                tag: Tag(self._client, self._repo, tag)
                for tag in self._client.get_repository_tags(self._repo)['tags']
            }
        return self.__tags

    def __getitem__(self, tag) -> Tag:
        return self._tags[tag]

    @property
    def tags(self) -> Iterable[Tag]:
        return self._tags.values()

    def __iter__(self) -> Iterable[Tag]:
        return iter(self.tags)

    @property
    def manifests(self) -> Set[Manifest]:
        return {tag.manifest for tag in self.tags}

    def delete(self) -> None:
        for manifest in self.manifests:
            manifest.delete()

    def __eq__(self, other) -> bool:
        return self._repo == other._repo and self.tags == other.tags


class Registry(Base):
    def __init__(self,
                 host: str,
                 verify_ssl: bool = False,
                 username: str = None,
                 password: str = None,
                 api_timeout: int = None):
        super().__init__(host)
        self._client: BaseClient = BaseClient(
            host=host,
            verify_ssl=verify_ssl,
            username=username,
            password=password,
            api_timeout=api_timeout,
        )

        self.__repositories: Union[Dict[str, Repository], None] = None

    @property
    def _repositories(self) -> Dict[str, Repository]:
        if self.__repositories is None:
            self.__repositories = {
                repo: Repository(self._client, repo)
                for repo in self._client.catalog()['repositories']
            }
        return self.__repositories

    def __getitem__(self, repository: str) -> Repository:
        return self._repositories[repository]

    @property
    def repositories(self) -> Iterable[Repository]:
        return self._repositories.values()

    def __iter__(self) -> Iterable[Repository]:
        return iter(self.repositories)
