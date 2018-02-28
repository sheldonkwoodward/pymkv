# pymkv 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e1fe077d95f74a5886c557024777c26c)](https://www.codacy.com/app/sheldonkwoodward/pymkv?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sheldonkwoodward/pymkv&amp;utm_campaign=Badge_Grade)

pymkv is a Python wrapper for mkvmerge. It provides support for muxing tracks together, combining multiple MKV files, reordering tracks, naming tracks, and other MKV related things.


## Installation
mkvmerge must be downloaded or installed on your computer. It is recommended to add it to your $PATH variable but a different path can be manually specified. mkvmerge can be found and downloaded from [here](https://mkvtoolnix.download/downloads.html).

To install pymkv using pip, run the following command in the projects root:
```
pip install .
```
The `-e` flag can be used during installation for code changes to updated automatically in pip.


## MKVFile
The MKVFile class is the core class of pymkv. This class can receive MKVTrack or MKVFile objects and mux them together.

An MKV file can be created using the MKVFile class:
```
mkv = MKVFile()
```

MKVFiles also have two optional arguments:

* **path** The path to an existing MKV file to be imported and used in the MKVFile. None by default.

* **title** String value to specify the internal file name. None by default but will use existing internal title if present.

Example:
```
file = MKVFile(path='path/to/file.mkv', title='Some title')
```

### Functions
#### command(output_file, subprocess=False)
The <b>command()</b> function uses the provided tracks and data to generate the relative mkvmerge command. This does not execute the command but only generates the command string. The <b>output_file</b> parameter will be the writing location used by the command.

There is an optional <b>subprocess</b> parameter that will return the command as a list so it can be easily executed using the subprocess module. The default is to return the command string.

By default the generated command will use 'mkvmerge' as the first argument in the command. If mkvmerge has not been added to your $PATH variable you will have to set the mkvmerge_path variable.

Example:
```
mkv.mkvmerge_path = 'path/to/mkvmerge'
```

#### mux(output_file, silent=False)
The mux function uses <b>command()</b> and the <b>subprocess</b> module to mux the currently specified file. The file will be written to the <b>output_file</b> location overwriting if necessary.

There is an optional <b>silent</b> argument that will suppress the mkvmerge output. By default, the output is shown.

#### add_track(track)
The <b>add_track()</b> function is used to add a track to the MKVFile. The <b>track</b> object or a path to a track is provided as an argument. A track_name can be supplied as an optional argument. The order in which the tracks are added is the same order that they are initially set to be in the MKV file. More info on creating tracks is available in the Tracks section.

Example:
```
mkv = MKVFile('path/to/mkv/file.mkv')
video = MKVTrack('path/to/video/track.h264')
mkv.add_track(video)
mkv.add_track('path/to/audio/track.aac', 'Audio track name')
```

#### add_file(file)
The <b>add_file()</b> function is used to import tracks from the specified <b>file</b> to another MKVFile. The <b>file</b> object or path to a file is provided as an argument. The tracks from the specified file are added to the end of the file list of the file that calls <b>add_file()</b>.

Example:
```
mkv_1 = MKVFile('path/to/mkv/file.mkv')
mkv_2 = MKVFile('path/to/another/mkv/file.mkv')
mkv_1.add_file(mkv_2)
mkv_1.add_file('path/to/a/third/mkv/file.mkv')
```

#### add_chapters(chapters, language=None)
The <b>add_file()</b> function is used to import a chapters file into the MKVFile. The path to a file is provided as an argument. Any chapters existing in an import MKV file will still remain in the muxed output unless they are excluded using <b>exclude_internal_chapters()</b>.

#### remove_track(track_num*)
The <b>remove_track()</b> function removes the track at the index <b>track_num</b>.

#### exclude_internal_chapters()
The <b>exclude_internal_chapters()</b> function will exclude all internal chapters of the currently specified MKVFile. Chapters will be included in the mux if they are added from an external file or if another file with non-excluded chapters is added using <b>add_track()</b>.

#### move_track_front(track_num*)
The <b>move_track_front()</b> function sets the track at the index <b>track_num</b> as the first track in the file.

#### move_track_end(track_num*)
The <b>move_track_end()</b> function sets the track at the index <b>track_num</b> as the last track in the file.

#### move_track_forward(track_num*)
The <b>move_track_forward()</b> function moves the track at the index <b>track_num</b> forward one position in the file.

#### move_track_backward(track_num*)
The <b>move_track_backward()</b> function moves the track at the index <b>track_num</b> backward one position in the file.

#### swap_tracks(track_num_1*, track_num_2*)
The <b>swap_tracks()</b> function swaps the tracks at the index <b>track_num_1</b> and <b>track_num_2</b> in the file.

<br>

\* The specified tracks must be in the range of the total number of tracks specified in the file. If the index is out of range, the command will be ignored.


## MKVTrack
MKV tracks are embodied by the MKVTrack class. In order to mux tracks together, you must use the <b>add_track()</b> function of an MKVFile.

The only required argument to create a track is the path to the track file:
```
track = MKVTrack('path/to/track.h264')
```

MKVTracks also have four optional arguments:

* **default_track** True or False value to specify if the track is the default track for its type. The first video or audio track in an MKV file will be the default track unless specified otherwise. False by default.

* **forced_track** True or False value to specify if the track is a forced track. False be default.

* **language** Sets the language of the track. Must be am ISO639-2 language code to work properly.

* **track_name** Sets the name of the track.

Example:
```
track = MKVTrack('path/to/track.h264', default_track=True, forced_track=False, language='eng', track_name='A cool new track')
```
