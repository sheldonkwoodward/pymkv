# pymkv
pymkv is a Python wrapper for mkvmerge, a part of the MKVToolNix suite. It currently provides support for muxing separate track files together into a single MKV file.


# MKVObject
The MKVObject class is the core class of pymkv. This class recieves Track objects and muxes them together.

The only required argument is the path to the output file. An MKVObject can be created using the MKVObject class:
```
mkv = MKVObject('path/to/output/file.mkv')
```

An optional title arguments can be included to set the internal name of the file:
```
mkv = MKVObject('path/to/output/file.mkv', title='Some Name Here')
```

## Functions
### command()
The command function uses the provided tracks and data to generate the relative mkvmerge command. This does not execute the command but only generates the command string.

### mux()
The mux function runs the command function and then executes the command using subprocess.run(). This functionality only works when mkvmerge has been added to your $PATH variable.

### add_track(track)
The add_track function is used to add a track to te MKVObject. The track object is provided as an argument. The order in which the tracks are added is the same order that they will be in the MKV file. More info on creating tracks is available in the Tracks section.

Example:
```
mkv = MKVObject('path/to/output/file.mkv')
video = Track('path/to/video/track.h264')
audio = Track('path/to/audio/track.aac')
mkv.add_track(video)
mkv.add_track(audio)
```


# Tracks
Tracks are embodied by the Track class or any of its specific subclasses.  In order to mux tracks together, you must create track instantiations and pass them to an MKVObject.

The only required argument is the path to the track file. A generic track can be created using the Track class:
```
track = Track('path/to/track.h264')
```

More specific tracks can be created using the VideoTrack, AudioTrack, or SubtitleTrack classes. As of now, there is no difference between them and they can all be used in the same way.

Tracks also have four optional arguments:

* **title** Sets the name of the track.

* **language** Sets the language of the track. Must follow the [MKV language convention](www.matroska.org/technical/specs/index.html#languages) to work properly.

* **default** True or False value to specify if the track is the default track for its type. The first video or audio track in an MKV file will be the default track unless specified otherwise. False by default.

* **forced** True or False value to specify if the track is a forced track. False be default.

Example:
```
track = Track('path/to/track.h264', title='Some Name Here', language='eng', default=False, forced=True)
```
