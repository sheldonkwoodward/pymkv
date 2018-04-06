pymkv
=====

|PyPI Version|
|Codacy Badge|
|License|

pymkv is a Python wrapper for mkvmerge. It provides support for muxing, splitting, linking, chapters, tags, and
and attachments through the use of mkvmerge.

About pymkv
-----------

pymkv is a Python 3 library for manipulating MKV files. I was previously constructing mkvmerge commands manually but
they were becoming overly complex and unmanageable. This is what inspired me to start this project. Please open
new issues for any bugs you find, support is greatly appreciated!

Installation
------------

mkvmerge must be installed on your computer. It is recommended to add it to your $PATH variable but a
different path can be manually specified. mkvmerge can be found and downloaded from
`here <https://mkvtoolnix.download/downloads.html>`__ or can be found in most package managers.

To install pymkv using pip, run the following command:

::

    $ pip install pymkv

or clone the repo and run the following command if you wish to edit the source code:

::

    $ pip install -e .

Documentation
-------------

pymkv documentation can be found in the `GitHub repo wiki <https://github.com/sheldonkwoodward/pymkv/wiki>`__.

.. |PyPI Version| image::  https://img.shields.io/pypi/sheldonkwoodward/pymkv.svg
    :target: https://pypi.python.org/pypi/pymkv/
    :alt: Latest Version in PyPI

.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/e1fe077d95f74a5886c557024777c26c
   :target: https://www.codacy.com/app/sheldonkwoodward/pymkv?utm_source=github.com&utm_medium=referral&utm_content=sheldonkwoodward/pymkv&utm_campaign=Badge_Grade

.. |License| image:: https://img.shields.io/github/license/sheldonkwoodward/pymkv.svg   :alt: GitHub license
    :target: https://github.com/sheldonkwoodward/pymkv/blob/develop/LICENSE.txt
