# pymkv
[![PyPI Version](https://img.shields.io/pypi/v/pymkv.svg)](https://pypi.python.org/pypi/pymkv)
[![License](https://img.shields.io/github/license/sheldonkwoodward/pymkv.svg)](https://github.com/sheldonkwoodward/pymkv/LICENSE.txt)
[![Code Quality](https://api.codacy.com/project/badge/Grade/e1fe077d95f74a5886c557024777c26c)](https://api.codacy.com/project/badge/Grade/e1fe077d95f74a5886c557024777c26c)

pymkv is a Python wrapper for mkvmerge and other tools in the MKVToolNix suite. It provides support for muxing,
splitting, linking, chapters, tags, and attachments through the use of mkvmerge.

## About pymkv
pymkv is a Python 3 library for manipulating MKV files with mkvmerge. Constructing mkvmerge commands manually can
quickly become confusing and complex. To remedy this, I decided to write this library to make mkvmerge more
scriptable and easier to use. Please open new issues for any bugs you find, support is greatly appreciated!

## Installation
mkvmerge must be installed on your computer, it is needed to process files when creating MKV objects. It is also
recommended to add it to your $PATH variable but a different path can be manually specified. mkvmerge can be found
and downloaded from [here](https://mkvtoolnix.download/downloads.html) or from most package managers.

To install pymkv from PyPI, use the following command:

    $ pip install pymkv

You can also clone the repo and run the following command in the project root to edit the source code:

    $ pip install -e .

## Documentation
The documentation for pymkv can be found [here](https://pymkv.shel.dev) or in the project's docstrings.

## Roadmap
pymkv was a project started a few years ago when I was first learning Python. There were a number of things that I
did that could use improvement. The planned changes and future features are outlined below. Keep an eye on the [Github
Projects page](https://github.com/sheldonkwoodward/pymkv/projects) for the current roadmap status.

### ~~Documentation~~
The current documentation for pymkv is lacking. Instead of manually managing a GitHub Wiki, Sphinx will be setup to
automatically generate documentation from docstrings. The docstrings will also need to be updated and improved to
ensure this documentation is complete.

### Tests
After completing documentation for the existing features, unit tests need to be written to "lock in" the existing
functionality. Generating mkvmerge commands can be complex and it is easy to subtly modify an existing feature when
adding a new one. Unit tests will ensure that features remain the same and help prevent bugs in the future.

### Cleanup
The existing code base could use some tidying, better commenting, debugging, and a general styling overhaul. Setting up
[pre-commit](https://pre-commit.com/) and the [Black code formatter](https://github.com/psf/black) will help keep the
code base more readable and maintainable.

### Features
Once these first three steps are complete, pymkv will be ready to start adding new features. The goal is for pymkv to
implement the functionality of mkvmerge and other MKVToolNix tools as closely as possible. New features and bugs will
be added to the [GitHub issues page](https://github.com/sheldonkwoodward/pymkv/issues). As pymkv progresses through
the previous steps, this roadmap will be expanded to outline new features.
