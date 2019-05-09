import os
import sys
from setuptools import setup  # type: ignore

# The directory containing this file
HERE = os.path.dirname(__file__)

# The text of the README file
README_FILE = (os.path.join(HERE, 'README.md'))
with open(README_FILE) as f:
    README = f.read()

requirements = [  # type: ignore
    'requests>=2.4.3, <3.0.0',
    'ecdsa>=0.13.0, <0.14.0',
    'jws>=0.1.3, <0.2.0',
]

if sys.version_info < (3, 5):
    requirements.append('typing')

# This call to setup() does all the work
setup(
    name='simple-registry-api',
    version='1.1.0',
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
    install_requires=requirements
)
