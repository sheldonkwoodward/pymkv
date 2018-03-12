# sheldon woodward
# 2/25/2018

"""MKVFile Class"""

import subprocess as sp
import json
from os.path import expanduser, isfile

from pymkv import MKVTrack


class MKVFile:
    def __init__(self, path=None, title=None):
        """A class that represents an MKV file.

        The MKVFile class can either import a pre-existing MKV file or create a new one. After an MKVFile object has
        been instantiated, MKVTracks or other MKVFile objects can be added using add_track() and add_file()
        respectively.

        Tracks are always added in the same order that they exist in a file or are added in. They can be reordered
        using move_track_front(), move_track_end(), move_track_forward(), move_track_backward(), or swap_tracks().

        After an MKVFile has been created, an mkvmerge command can be generated using command() or the file can be
        muxed using mux().

        path (str, optional):
            Path to a pre-existing MKV file. The file will be imported into the new MKVFile object.
        title (str, optional):
            The internal title given to the MKVFile. If no title is given, the title of the pre-existing file will
            be used if it exists.
        """
        self.mkvmerge_path = 'mkvmerge'
        self.path = None
        if path:
            self.path = expanduser(path)
        self.title = title
        self.chapters = None
        self.chapter_language = None
        self.tracks = []
        if path:
            # add file title
            info_json = json.loads(sp.check_output([self.mkvmerge_path, '-J', self.path]).decode('utf8'))
            if not self.title and 'title' in info_json['container']['properties']:
                self.title = info_json['container']['properties']['title']

            # add tracks with info
            for track in info_json['tracks']:
                new_track = MKVTrack(self.path)
                new_track.track_id = track['id']
                if 'default_track' in track['properties']:
                    new_track.default_track = track['properties']['default_track']
                if 'forced_track' in track['properties']:
                    new_track.forced_track = track['properties']['forced_track']
                if 'language' in track['properties']:
                    new_track.language = track['properties']['language']
                if 'track_name' in track['properties']:
                    new_track.track_name = track['properties']['track_name']
                self.add_track(new_track)

    def command(self, output_file, subprocess=False):
        """Generates an mkvmerge command based on the configured MKVFile.

        output_file (str):
            The path to be used as the output file in the mkvmerge command.
        subprocess (bool):
            Will return the command as a list so it can be used easily with the subprocess module.

        Returns:
            Returns the command to create the specified MKV file. Return type is str by default. Will return as list if
            subprocess is true.
        """
        command = [self.mkvmerge_path, '-o', expanduser(output_file)]
        if self.title:
            command.extend(['--title', self.title])
        # add tracks
        for track in self.tracks:
            # flags
            if track.track_name:
                command.extend(['--track-name', str(track.track_id) + ':' + track.track_name])
            if track.language:
                command.extend(['--language', str(track.track_id) + ':' + track.language])
            if not track.default_track:
                command.extend(['--default-track', str(track.track_id) + ':0'])
            if track.forced_track:
                command.extend(['--forced-track', str(track.track_id) + ':1'])

            # remove extra tracks
            if track.track_type != 'video':
                command.append('-D')
            else:
                command.extend(['-d', str(track.track_id)])
            if track.track_type != 'audio':
                command.append('-A')
            else:
                command.extend(['-a', str(track.track_id)])
            if track.track_type != 'subtitles':
                command.append('-S')
            else:
                command.extend(['-s', str(track.track_id)])

            # exclude chapters
            if track.exclude_chapters:
                command.append('--no-chapters')

            # add path
            command.append(track.path)

        # chapters
        if self.chapter_language:
            command.extend(['--chapter-language', self.chapter_language])
        if self.chapters:
            command.extend(['--chapters', self.chapters])

        if subprocess:
            return command
        return " ".join(command)

    def mux(self, output_file, silent=False):
        """Muxes the specified MKVFile.

        output_file (str):
            The path to be used as the output file in the mkvmerge command.
        silent (bool):
            By default the mkvmerge output will be shown unless silent is True.
        """
        if silent:
            sp.check_output(self.command(expanduser(output_file), subprocess=True))
        else:
            command = self.command(expanduser(output_file))
            print('Running with command:\n"' + command + '"')
            sp.run(self.command(expanduser(output_file), subprocess=True))

    def add_track(self, track, track_name=None):
        """Add an MKVTrack to the MKVFile.

        track (str, MKVTrack):
            The MKVTrack to be added the MKVFile.
        track_name (str, optional):
            The name of the new track. Will override any previous name.
        """
        if isinstance(track, str):
            new_track = MKVTrack(track, track_name=track_name)
            self.tracks.append(new_track)
        elif isinstance(track, MKVTrack):
            if track_name:
                track.track_name = track_name
            self.tracks.append(track)
        else:
            raise TypeError('track is not str or MKVTrack')

    def add_file(self, file):
        """Combine an MKVFile with another MKVFile.

        file (MKVFile):
            The MKVFile to be combined with the MKVFile.
        """
        if isinstance(file, str):
            new_file = MKVFile(file)
            self.tracks = self.tracks + new_file.tracks
        elif isinstance(file, MKVFile):
            self.tracks = self.tracks + file.tracks
        else:
            raise TypeError('track is not str or MKVFile')

    def add_chapters(self, chapters, language=None):
        """Add a chapters file to an MKVFile.

        chapters (str):
            The chapters file to be added to the MKVFile.
        language (str, optional):
            Must be an ISO639-2 language code. Only works if no existing language information exists in chapters.
        """
        self.chapters = expanduser(chapters)
        if not isfile(self.chapters):
            raise FileNotFoundError('file specified does not exist')
        if language:
            if language in open('ISO639-2.txt').read():
                self.chapter_language = language
            else:
                raise ValueError('not an ISO639-2 language code')

    def remove_track(self, track_num):
        """Remove a track from the MKVFile.

        track_num (int):
            The track number of the track to remove.
        """
        if 0 <= track_num < len(self.tracks):
            del self.tracks[track_num]
        else:
            raise IndexError('track index out of range')

    def exclude_internal_chapters(self):
        """Ignore the internal subtitles of the MKVFile"""
        for track in self.tracks:
            track.exclude_chapters = True

    def get_track(self, track_num=None):
        """Get a track from the MKVFile.

        index (int):
            Index of track to retrieve. Will return list if argument is not provided.
        """
        if track_num is None:
            return self.tracks
        else:
            return self.tracks[track_num]

    def move_track_front(self, track_num):
        """Set a track as the first in an MKVFile.

        track_num (int):
            The track number of the track to move to the front.
        """
        if 0 <= track_num < len(self.tracks):
            self.tracks.insert(0, self.tracks.pop(self.tracks[track_num]))
        else:
            raise IndexError('track index out of range')

    def move_track_end(self, track_num):
        """Set as track as the last in an MKVFile.

        track_num (int):
            The track number of the track to move to the back.
        """
        if 0 <= track_num < len(self.tracks):
            self.tracks.append(self.tracks.pop(self.tracks[track_num]))
        else:
            raise IndexError('track index out of range')

    def move_track_forward(self, track_num):
        """Move a track forward in an MKVFile.

        track_num (int):
            The track number of the track to move forward.
        """
        if 0 <= track_num < len(self.tracks) - 1:
            self.tracks[track_num], self.tracks[track_num + 1] = self.tracks[track_num + 1], self.tracks[track_num]
        else:
            raise IndexError('track index out of range')

    def move_track_backward(self, track_num):
        """Move a track backward in an MKVFile.

        track_num (int):
            The track number of the track to move backward.
        """
        if 0 < track_num < len(self.tracks):
            self.tracks[track_num], self.tracks[track_num - 1] = self.tracks[track_num - 1], self.tracks[track_num]
        else:
            raise IndexError('track index out of range')

    def swap_tracks(self, track_num_1, track_num_2):
        """Swap the position of two tracks in an MKVFile.

        track_num_1 (int):
            The track number of one track to swap.
        track_num_2 (int):
            The track number of the other track to swap
        """
        if 0 <= track_num_1 < len(self.tracks) and 0 <= track_num_2 < len(self.tracks):
            self.tracks[track_num_1], self.tracks[track_num_2] = self.tracks[track_num_2], self.tracks[track_num_1]
        else:
            raise IndexError('track index out of range')

    def replace_track(self, track_num, track):
        """Replace a track with another track in an MKVFile.

        track_num (int):
            The track number of the track to replace.
        track (MKVTrack):
            The MKVTrack to be replaced into the file.
        """
        if 0 <= track_num < len(self.tracks):
            self.tracks[track_num] = track
        else:
            raise IndexError('track index out of range')
