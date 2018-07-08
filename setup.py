from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sys
import os
import re


here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

def read(*parts):
    with open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("dictances", "__version__.py")

setup(
    name="smallMITM",
    version=__version__,
    author="Tommaso Fontana",
    author_email="tommaso.fontana.96@gmail.com",
    license='MIT',
    description="Easy to setup and configure package to do Man-In-The-Middle.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zommiommy/smallMITM",
    packages=setuptools.find_packages(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*'])
)

def status(s):
    print('\033[1m{0}\033[0m'.format(s))


status('Pushing git tags…')
os.system('git tag v{0}'.format(__version__))
os.system('git push --tags')
