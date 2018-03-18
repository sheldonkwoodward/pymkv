# sheldon woodward
# 2/25/2018

"""MKVTrack Class"""

import subprocess as sp
import json
from os.path import expanduser

from pymkv.ISO639_2 import ISO639_2 as LANGUAGES


class MKVTrack:
    def __init__(self, path, mkvmerge_path='mkvmerge', default_track=False, forced_track=False, language=None,
                 track_name=None, exclude_chapters=False, track_id=0):
        """An class that represents an MKV track such as video, audio, or subtitles.

        MKVTracks can be added to an MKVFile. MKVTracks can be video, audio, or subtitle tracks. The only required
        argument is path which gives the path to a track file.

        path (str):
            Path to the track file.
        default_track (bool, optional):
            Determines if the track should be the default track of its type when muxed into an MKV file.
        forced_track (bool, optional):
            Determines if the track should be a forced track when muxed into an MKV file.
        language (str, optional):
            The language of the track. It must follow the guidelines specified here:
            www.matroska.org/technical/specs/index.html#languages
        track_name (str, optional):
            The name that will be given to the track when muxed into a file.
        """
        self.path = expanduser(path)
        self.mkvmerge_path = mkvmerge_path
        self.default_track = default_track
        self.forced_track = forced_track
        self._language = None
        self.language = language
        self.track_name = track_name
        self.exclude_chapters = exclude_chapters
        self._track_id = track_id
        info_json = json.loads(sp.check_output([mkvmerge_path, '-J', self.path]).decode('utf8'))
        self.track_type = info_json['tracks'][self._track_id]['type']

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        if language in LANGUAGES or language is None:
            self._language = language
        else:
            raise ValueError('not an ISO639-2 language code')

    @property
    def track_id(self):
        return self._track_id

    @track_id.setter
    def track_id(self, track_id):
        self._track_id = track_id
        info_json = json.loads(sp.check_output([self.mkvmerge_path, '-J', self.path]).decode('utf8'))
        self.track_type = info_json['tracks'][self._track_id]['type']
