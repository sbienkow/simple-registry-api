import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setup(
    name='simple-registry-api',
    version='1.0.0',
    description='Simple docker registry API',
    keywords='docker docker-registry docker-image REST',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/sbienkow/simple-registry-api',
    author='sbienkow',
    author_email='sbienkow@gmail.com',
    license='GNU GPLv3+',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['simple_registry_api'],
    include_package_data=True,
    install_requires=[
        'docker-registry-client >= 0.5.2'
    ]
)
