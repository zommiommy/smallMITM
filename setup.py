import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smallMITM",
    version="0.0.1",
    author="Tommaso Fontana",
    author_email="tommaso.fontana.96@gmail.com",
    description="Easy to setup and configure package to do Man-In-The-Middle.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zommiommy/smallMITM",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
