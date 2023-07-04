pymkv
=====

Welcome to the pymkv documentation! Here you will find links to the core modules and examples of how to use each.

Modules
-------

The three primary modules of pymkv are :class:`~pymkv.MKVFile`, :class:`~pymkv.MKVTrack`, and
:class:`~pymkv.MKVAttachment`. The :class:`~pymkv.MKVFile` class is used to import existing or create new MKV files.
The :class:`~pymkv.MKVTrack` class is used to add individual tracks to an :class:`~pymkv.MKVFile`. The
:class:`~pymkv.MKVAttachment` class is used to add attachments to an :class:`~pymkv.MKVFile`.

Each module supports or mimics many of the same operations as mkvmerge but are not necessarily complete. If there is
functionality that is missing or an error in the docs, please open a new issue `here <https://github
.com/gitbib/pymkv/issues>`_.

.. toctree::
    :maxdepth: 1

    pymkv/MKVFile
    pymkv/MKVTrack
    pymkv/MKVAttachment

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
