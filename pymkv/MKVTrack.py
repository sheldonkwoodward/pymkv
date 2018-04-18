# sheldon woodward
# 2/25/2018

"""MKVTrack Class"""

import json
from os.path import expanduser, isfile
import subprocess as sp

from pymkv.ISO639_2 import ISO639_2 as LANGUAGES
from pymkv.Verifications import verify_supported


class MKVTrack:
    def __init__(self, file_path, track_id=0, track_name=None, language=None, default_track=False, forced_track=False):
        """A class that represents an MKV track such as video, audio, or subtitles.

        MKVTracks can be added to an MKVFile. MKVTracks can be video, audio, or subtitle tracks. The only required
        argument is path which gives the path to a track file.

        file_path (str):
            Path to the track file. This can also be an MKV where the *track_id* is the track represented in the MKV.
            This is the only required argument.
        track_id (int, optional):
            The id of the track to be used in the file. Does not need to be set unless the input file has multiple
            tracks.
        track_name (str, optional):
            The name that will be given to the track when muxed into a file.
        language (str, optional):
            The language of the track. It must be an ISO639-2 language code.
        default_track (bool, optional):
            Determines if the track should be the default track of its type when muxed into an MKV file.
        forced_track (bool, optional):
            Determines if the track should be a forced track when muxed into an MKV file.
        """
        # track info
        self._track_codec = None
        self._track_type = None

        # base
        self.mkvmerge_path = 'mkvmerge'
        self._file_path = None
        self.file_path = file_path
        self._track_id = None
        self.track_id = track_id

        # flags
        self.track_name = track_name
        self._language = None
        self.language = language
        self._tags = None
        self.default_track = default_track
        self.forced_track = forced_track

        # exclusions
        self.no_chapters = False
        self.no_global_tags = False
        self.no_track_tags = False
        self.no_attachments = False

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        file_path = expanduser(file_path)
        if not verify_supported(file_path):
            raise ValueError('"{}" is not a supported file')
        self._file_path = file_path
        self.track_id = 0

    @property
    def track_id(self):
        return self._track_id

    @track_id.setter
    def track_id(self, track_id):
        info_json = json.loads(sp.check_output([self.mkvmerge_path, '-J', self.file_path]).decode())
        if not 0 <= track_id < len(info_json['tracks']):
            raise IndexError('track index out of range')
        self._track_id = track_id
        self._track_codec = info_json['tracks'][track_id]['codec']
        self._track_type = info_json['tracks'][track_id]['type']

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
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, file_path):
        if not isinstance(file_path, str):
            raise TypeError('"{}" is not of type str'.format(file_path))
        file_path = expanduser(file_path)
        if not isfile(file_path):
            raise FileNotFoundError('"{}" does not exist'.format(file_path))
        self._tags = file_path

    @property
    def track_codec(self):
        return self._track_codec

    @property
    def track_type(self):
        return self._track_type
