# Unda Development Branch
[![Downloads](https://static.pepy.tech/badge/unda)](https://pepy.tech/project/unda)
![Monthly Downloads](https://img.shields.io/pypi/dm/unda.svg?style=flat)
![GitHub forks](https://img.shields.io/github/forks/definite-d/unda?logo=github&style=flat)
![PyPi Version](https://img.shields.io/pypi/v/unda?style=flat)
![Python Versions](https://img.shields.io/pypi/pyversions/unda.svg?style=flat&logo=python])
![License](https://img.shields.io/pypi/l/unda.svg?style=flat&version=latest)

````text
pip install --upgrade unda
````

[Project Download Metrics](https://pepy.tech/project/Unda)

[Official Documentation](https://definite-d.github.io/unda/)

This branch is intended to serve as both the bleeding, unstable edge of this project's development, as well as a bootstrap for willing contributors to the project, containing nearly all files and resources used in development.


## Development/Contributor's Guide
This (brief) guide will assume: 
* a basic knowledge of Python and [how Python packaging works](https://packaging.python.org/), 
* basic `git` knowledge or skill with using GitHub repositories,
* and a terminal that can run `.bat` files (Windows).

### Basics
* Clone this branch
* Refrain from modifying the folder structure of the project too much unless you can apply the changes manually to 
the `publish.py`, `tester.py` and `generate_docs.bat` files.
* Modify the source code within the `unda` folder.
* *Very Important: Update the version number!* This project uses [semantic versioning](https://semver.org).
* *Run `tester.py` to be sure everything works.*
* Generate docs by running `generate_docs.bat`, _especially_ if you alter any docstrings; the documentation is auto-generated from 
them using [pdoc](https://github.com/pdoc3/pdoc).

### Building
* Within a terminal with the project folder set as the working directory, run `python -m publish.py build` to build the project.

### Publishing to PyPi
* This part requires a PyPi token. Should the need arise, I will personally administer upload tokens for legacy (main) uploads.
* Put the token (as a string) as the value of the `TOKEN` variable in the `publish.py` file and save.
* Run `python -m publish.py upload` from a command line to upload the built project, or run `python -m publish.py complete`
to build and upload automatically. Make sure you have an internet connection, otherwise the upload will not work.
* *The `publish.py` CLI can also be used in this format: `python -m publish.py --upload_to 'test' upload` to upload to TestPyPi
instead.* [Using TestPyPi itself](https://packaging.python.org/en/latest/guides/using-testpypi/) however, is beyond the scope of this guide.

## Finally...
...thank you for your time and efforts invested in this project as a contributor.
I hope you enjoy the process of developing unda as much as I do.

Divine.
