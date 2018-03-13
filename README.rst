pymkv
=====

|Codacy Badge|

pymkv is a Python wrapper for mkvmerge. It provides support for muxing
tracks together, combining multiple MKV files, reordering tracks, naming
tracks, and other MKV related things.

Installation
------------

mkvmerge must be downloaded or installed on your computer. It is
recommended to add it to your $PATH variable but a different path can be
manually specified. mkvmerge can be found and downloaded from
`here <https://mkvtoolnix.download/downloads.html>`__.

To install pymkv using pip, run the following command in the projects
root:

::

    pip install .

The ``-e`` flag can be used during installation for code changes to
updated automatically in pip.

MKVFile
-------

The MKVFile class is the core class of pymkv. This class can receive
MKVTrack or MKVFile objects and mux them together.

An MKV file can be created using the MKVFile class:

::

    mkv = MKVFile()

MKVFiles also have two optional arguments:

-  **path** The path to an existing MKV file to be imported and used in
   the MKVFile. None by default.

-  **title** String value to specify the internal file name. None by
   default but will use existing internal title if present.

Example:

::

    file = MKVFile(path='path/to/file.mkv', title='Some title')

Functions
~~~~~~~~~

command(output\_file, subprocess=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The command() function uses the provided tracks and data to generate the
relative mkvmerge command. This does not execute the command but only
generates the command string. The output\_file parameter will be the
writing location used by the command.

There is an optional subprocess parameter that will return the command
as a list so it can be easily executed using the subprocess module. The
default is to return the command string.

By default the generated command will use 'mkvmerge' as the first
argument in the command. If mkvmerge has not been added to your $PATH
variable you will have to set the mkvmerge\_path variable.

Example:

::

    mkv.mkvmerge_path = 'path/to/mkvmerge'

mux(output\_file, silent=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The mux function uses command() and the subprocess module to mux the
currently specified file. The file will be written to the output\_file
location overwriting if necessary.

There is an optional silent argument that will suppress the mkvmerge
output. By default, the output is shown.

add\_track(track)
^^^^^^^^^^^^^^^^^

The add\_track() function is used to add a track to the MKVFile. The
track object or a path to a track is provided as an argument. A
track\_name can be supplied as an optional argument. The order in which
the tracks are added is the same order that they are initially set to be
in the MKV file. More info on creating tracks is available in the Tracks
section.

Example:

::

    mkv = MKVFile('path/to/mkv/file.mkv')
    video = MKVTrack('path/to/video/track.h264')
    mkv.add_track(video)
    mkv.add_track('path/to/audio/track.aac', 'Audio track name')

add\_file(file)
^^^^^^^^^^^^^^^

The add\_file() function is used to import tracks from the specified
file to another MKVFile. The file object or path to a file is provided
as an argument. The tracks from the specified file are added to the end
of the file list of the file that calls add\_file().

Example:

::

    mkv_1 = MKVFile('path/to/mkv/file.mkv')
    mkv_2 = MKVFile('path/to/another/mkv/file.mkv')
    mkv_1.add_file(mkv_2)
    mkv_1.add_file('path/to/a/third/mkv/file.mkv')

add\_chapters(chapters, language=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The add\_file() function is used to import a chapters file into the
MKVFile. The path to a file is provided as an argument. Any chapters
existing in an import MKV file will still remain in the muxed output
unless they are excluded using exclude\_internal\_chapters().

remove\_track(track\_num\*) The remove\_track() function removes the track at the index track\_num.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

exclude\_internal\_chapters()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The exclude\_internal\_chapters() function will exclude all internal
chapters of the currently specified MKVFile. Chapters will be included
in the mux if they are added from an external file or if another file
with non-excluded chapters is added using add\_track().

get\_track(track\_num\*) STUB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

move\_track\_front(track\_num\*) The move\_track\_front() function sets the track at the index track\_num as the first track in the file.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

move\_track\_end(track\_num\*) The move\_track\_end() function sets the track at the index track\_num as the last track in the file.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

move\_track\_forward(track\_num\*) The move\_track\_forward() function moves the track at the index track\_num forward one position in the file.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

move\_track\_backward(track\_num\*) The move\_track\_backward() function moves the track at the index track\_num backward one position in the file.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

swap\_tracks(track\_num\_1\ *, track\_num\_2*)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The swap\_tracks() function swaps the tracks at the index track\_num\_1
and track\_num\_2 in the file.

replace\_track(track\_num\*, track) STUB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

\* The specified tracks must be in the range of the total number of
tracks specified in the file. If the index is out of range, the command
will be ignored.

MKVTrack
--------

MKV tracks are embodied by the MKVTrack class. In order to mux tracks
together, you must use the add\_track() function of an MKVFile.

The only required argument to create a track is the path to the track
file:

::

    track = MKVTrack('path/to/track.h264')

MKVTracks also have four optional arguments:

-  **default\_track** True or False value to specify if the track is the
   default track for its type. The first video or audio track in an MKV
   file will be the default track unless specified otherwise. False by
   default.

-  **forced\_track** True or False value to specify if the track is a
   forced track. False be default.

-  **language** Sets the language of the track. Must be am ISO639-2
   language code to work properly.

-  **track\_name** Sets the name of the track.

Example:

::

    track = MKVTrack('path/to/track.h264', default_track=True, forced_track=False, language='eng', track_name='A cool new track')

.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/e1fe077d95f74a5886c557024777c26c
   :target: https://www.codacy.com/app/sheldonkwoodward/pymkv?utm_source=github.com&utm_medium=referral&utm_content=sheldonkwoodward/pymkv&utm_campaign=Badge_Grade