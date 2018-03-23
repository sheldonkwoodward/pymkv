# sheldon woodward
# 2/25/2018

"""MKVFile Class"""

import subprocess as sp
import json
from os.path import expanduser, isfile

import bitmath

from pymkv.MKVTrack import MKVTrack
from pymkv.Timestamp import Timestamp
from pymkv.ISO639_2 import ISO639_2 as LANGUAGES


class MKVFile:
    def __init__(self, file_path=None, title=None):
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
        self.title = title
        self.chapters_file = None
        self.chapter_language = None
        self.tracks = []
        if file_path is not None:
            file_path = expanduser(file_path)
            if not MKVFile.verify_matroska(file_path):
                raise ValueError('"{}" is not a matroska file'.format(file_path))

            # add file title
            # TODO: change to properties
            info_json = json.loads(sp.check_output([self.mkvmerge_path, '-J', file_path]).decode('utf8'))
            if not self.title and 'title' in info_json['container']['properties']:
                self.title = info_json['container']['properties']['title']

            # add tracks with info
            for track in info_json['tracks']:
                new_track = MKVTrack(file_path, track_id=track['id'])
                if 'track_name' in track['properties']:
                    new_track.track_name = track['properties']['track_name']
                if 'language' in track['properties']:
                    new_track.language = track['properties']['language']
                if 'default_track' in track['properties']:
                    new_track.default_track = track['properties']['default_track']
                if 'forced_track' in track['properties']:
                    new_track.forced_track = track['properties']['forced_track']
                self.add_track(new_track)

        # options
        self._split_options = []
        self._link_to_previous_options = []
        self._link_to_next_options = []

    def command(self, output_path, subprocess=False):
        """Generates an mkvmerge command based on the configured MKVFile.

        output_file (str):
            The path to be used as the output file in the mkvmerge command.
        subprocess (bool):
            Will return the command as a list so it can be used easily with the subprocess module.

        Returns:
            Returns the command to create the specified MKV file. Return type is str by default. Will return as list if
            subprocess is true.
        """
        output_path = expanduser(output_path)
        command = [self.mkvmerge_path, '-o', output_path]
        if self.title:
            command.extend(['--title', self.title])
        # add tracks
        for track in self.tracks:
            # flags
            if track.track_name is not None:
                command.extend(['--track-name', str(track.track_id) + ':' + track.track_name])
            if track.language is not None:
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
            command.append(track.file_path)

        # chapters
        if self.chapter_language is not None:
            command.extend(['--chapter-language', self.chapter_language])
        if self.chapters_file is not None:
            command.extend(['--chapters', self.chapters_file])

        # split options
        command.extend(self._split_options)
        command.extend(self._link_to_previous_options)
        command.extend(self._link_to_next_options)

        if subprocess:
            return command
        return " ".join(command)

    def mux(self, output_path, silent=False):
        """Muxes the specified MKVFile.

        output_file (str):
            The path to be used as the output file in the mkvmerge command.
        silent (bool):
            By default the mkvmerge output will be shown unless silent is True.
        """
        output_path = expanduser(output_path)
        if silent:
            sp.check_output(self.command(output_path, subprocess=True))
        else:
            command = self.command(output_path)
            print('Running with command:\n"' + command + '"')
            sp.run(self.command(output_path, subprocess=True))

    def add_track(self, track):
        """Add an MKVTrack to the MKVFile.

        track (str, MKVTrack):
            The MKVTrack to be added the MKVFile.
        """
        if isinstance(track, str):
            self.tracks.append(MKVTrack(track))
        elif isinstance(track, MKVTrack):
            self.tracks.append(track)
        else:
            raise TypeError('track is not str or MKVTrack')

    def add_file(self, file):
        """Combine an MKVFile with another MKVFile.

        file (MKVFile):
            The MKVFile to be combined with the MKVFile.
        """
        if isinstance(file, str):
            self.tracks = self.tracks + MKVFile(file).tracks
        elif isinstance(file, MKVFile):
            self.tracks = self.tracks + file.tracks
        else:
            raise TypeError('track is not str or MKVFile')

    def add_chapters(self, file_path, language=None):
        """Add a chapters file to an MKVFile.

        chapters (str):
            The chapters file to be added to the MKVFile.
        language (str, optional):
            Must be an ISO639-2 language code. Only works if no existing language information exists in chapters.
        """
        if not isinstance(file_path, str):
            raise TypeError('"{}" is not of type str'.format(file_path))
        file_path = expanduser(file_path)
        if not isfile(file_path):
            raise FileNotFoundError('"{}" does not exist'.format(file_path))
        self.chapters_file = file_path
        if language is not None and language not in LANGUAGES:
            raise ValueError('not an ISO639-2 language code')
        elif language is not None and language in LANGUAGES:
                self.chapter_language = language

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

    def remove_track(self, track_num):
        """Remove a track from the MKVFile.

        track_num (int):
            The track number of the track to remove.
        """
        if 0 <= track_num < len(self.tracks):
            del self.tracks[track_num]
        else:
            raise IndexError('track index out of range')

    def split_none(self):
        """Remove all splitting options."""
        self._split_options = []

    def split_size(self, size, link=False):
        """Split the output file into parts by size.

        size (bitmath obj, int):
            The size of each split file. Takes either a bitmath size object or an integer representing the number of
            bytes.
        """
        if getattr(size, '__module__', None) == bitmath.__name__:
            size = size.bytes
        elif not isinstance(size, int):
            raise TypeError('size is not a bitmath object or integer')
        self._split_options = ['--split', 'size:{}'.format(size)]
        if link:
            self._split_options += '--link'

    def split_duration(self, duration, link=False):
        """Split the output file into parts by duration.

        duration (str, int):
            The duration of each split file. Takes either a str formatted to HH:MM:SS.nnnnnnnnn or an integer
            representing the number of seconds. The duration string requires formatting of at least M:S.
        """
        self._split_options = ['--split', 'duration:' + str(Timestamp(duration))]
        if link:
            self._split_options += '--link'

    def split_timestamps(self, *timestamps, link=False):
        """Split the output file into parts by timestamps.

        *timestamps (str, int, list, tuple):
            The timestamps to split the file by. Can be passed as any combination of strs and ints, inside or outside
            an Iterable object. Any lists will be flattened. Timestamps must be ints, representing seconds, or strs in
            the form HH:MM:SS.nnnnnnnnn. The timestamp string requires formatting of at least M:S.
        """
        # check if in timestamps form
        ts_flat = MKVFile.flatten(timestamps)
        if len(ts_flat) == 0:
            raise ValueError('"{}" are not properly formatted timestamps'.format(timestamps))
        if None in ts_flat:
            raise ValueError('"{}" are not properly formatted timestamps'.format(timestamps))
        for ts_1, ts_2 in zip(ts_flat[:-1], ts_flat[1:]):
            if Timestamp(ts_1) >= Timestamp(ts_2):
                raise ValueError('"{}" are not properly formatted timestamps'.format(timestamps))

        # build ts_string from timestamps
        ts_string = 'timestamps:'
        for ts in ts_flat:
            ts_string += str(Timestamp(ts)) + ','
        self._split_options = ['--split', ts_string[:-1]]
        if link:
            self._split_options += '--link'

    def split_frames(self, *frames, link=False):
        """Split the output file into parts by frames.

        *frames (int, list, tuple):
            The frames to split the file by. Can be passed as any combination of ints, inside or outside an Iterable
            object. Any lists will be flattened. Frames must be ints.
        """
        # check if in frames form
        f_flat = MKVFile.flatten(frames)
        if len(f_flat) == 0:
            raise ValueError('"{}" are not properly formatted frames'.format(frames))
        for f in f_flat:
            if not isinstance(f, int):
                raise TypeError('frame "{}" not an int'.format(f))
        for f_1, f_2 in zip(f_flat[:-1], f_flat[1:]):
            if f_1 >= f_2:
                raise ValueError('"{}" are not properly formatted frames'.format(frames))

        # build f_string from frames
        f_string = 'frames:'
        for f in f_flat:
            f_string += str(f) + ','
        self._split_options = ['--split', f_string[:-1]]
        if link:
            self._split_options += '--link'

    def split_timestamp_parts(self, timestamp_parts, link=False):
        """Split the output in parts by time parts.

        parts (list, tuple):
            An Iterable of timestamp sets. Each timestamp set should be an Iterable of an even number of timestamps
            or any number of timestamp pairs. The very first and last timestamps are permitted to be None. Timestamp
            sets containing 4 or more timestamps will output as one file containing the parts specified.
        """
        # check if in parts form
        ts_flat = MKVFile.flatten(timestamp_parts)
        if len(timestamp_parts) == 0:
            raise ValueError('"{}" are not properly formatted parts'.format(timestamp_parts))
        if None in ts_flat[1:-1]:
            raise ValueError('"{}" are not properly formatted parts'.format(timestamp_parts))
        for ts_1, ts_2 in zip(ts_flat[:-1], ts_flat[1:]):
            if None not in (ts_1, ts_2) and Timestamp(ts_1) >= Timestamp(ts_2):
                raise ValueError('"{}" are not properly formatted parts'.format(timestamp_parts))

        # build ts_string from parts
        ts_string = 'parts:'
        for ts_set in timestamp_parts:
            # flatten set
            ts_set = MKVFile.flatten(ts_set)

            # check if in set form
            if not isinstance(ts_set, (list, tuple)):
                raise TypeError('set is not of type list or tuple')
            if len(ts_set) < 2 or len(ts_set) % 2 != 0:
                raise ValueError('"{}" is not a properly formatted set'.format(ts_set))

            # build parts from sets
            for index, ts in enumerate(ts_set):
                # check for combined split
                if index % 2 == 0 and index > 0:
                    ts_string += '+'
                # add timestamp if not None
                if ts is not None:
                    ts_string += str(Timestamp(ts))
                # add ',' or '-'
                ts_string += '-' if index % 2 == 0 else ','
        self._split_options = ['--split', ts_string[:-1]]
        if link:
            self._split_options += '--link'

    def split_parts_frames(self, frame_parts, link=False):
        """Split the output in parts by frames.

        parts (list, tuple):
            An Iterable of frame sets. Each frame set should be an Iterable of an even number of frames or any
            number of frame pairs. The very first and last frames are permitted to be None. Frame sets containing 4
            or more frames will output as one file containing the parts specified.
        """
        # check if in parts form
        f_flat = MKVFile.flatten(frame_parts)
        if len(frame_parts) == 0:
            raise ValueError('"{}" are not properly formatted parts'.format(frame_parts))
        if None in f_flat[1:-1]:
            raise ValueError('"{}" are not properly formatted parts'.format(frame_parts))
        for f_1, f_2 in zip(f_flat[:-1], f_flat[1:]):
            if None not in (f_1, f_2) and f_1 >= f_2:
                raise ValueError('"{}" are not properly formatted parts'.format(frame_parts))

        # build f_string from parts
        f_string = 'parts:'
        for f_set in frame_parts:
            # flatten set
            f_set = MKVFile.flatten(f_set)

            # check if in set form
            if not isinstance(f_set, (list, tuple)):
                raise TypeError('set is not of type list or tuple')
            if len(f_set) < 2 or len(f_set) % 2 != 0:
                raise ValueError('"{}" is not a properly formatted set'.format(f_set))

            # build parts from sets
            for index, f in enumerate(f_set):
                # check if frames are ints
                if not isinstance(f, int) and f is not None:
                    raise TypeError('frame "{}" not an int'.format(f))

                # check for combined split
                if index % 2 == 0 and index > 0:
                    f_string += '+'
                # add frame if not None
                if f is not None:
                    f_string += str(f)
                # add ',' or '-'
                f_string += '-' if index % 2 == 0 else ','
        self._split_options = ['--split', f_string[:-1]]
        if link:
            self._split_options += '--link'

    def split_chapters(self, *chapters, link=False):
        """Split the output file into parts by chapters.

       *chapters (int, list, tuple):
           The chapters to split the file by. Can be passed as any combination of ints, inside or outside an
           Iterable object. Any lists will be flattened. Chapters must be ints.
       """
        # check if in chapters form
        c_flat = MKVFile.flatten(chapters)
        if len(chapters) == 0:
            self._split_options = ['--split', 'chapters:all']
            return
        for c in c_flat:
            if not isinstance(c, int):
                raise TypeError('chapter "{}" not an int'.format(c))
            if c < 1:
                raise ValueError('"{}" are not properly formatted chapters'.format(chapters))
        for c_1, c_2 in zip(c_flat[:-1], c_flat[1:]):
            if c_1 >= c_2:
                raise ValueError('"{}" are not properly formatted chapters'.format(chapters))

        # build c_string from chapters
        c_string = 'chapters:'
        for c in c_flat:
            c_string += str(c) + ','
        self._split_options = ['--split', c_string[:-1]]
        if link:
            self._split_options += '--link'

    def link_to_none(self):
        """Remove all linking to previous and next options."""
        self._link_to_previous_options = []
        self._link_to_next_options = []

    def link_to_previous(self, file_path):
        """Link the output file as the predecessor of the file_path file.

        file_path (str):
            Path of the file to be linked to.
        """
        # check if valid file
        if not isinstance(str, file_path):
            raise TypeError('"{}" is not of type str'.format(file_path))
        file_path = expanduser(file_path)
        if not MKVFile.verify_matroska(file_path):
            raise ValueError('"{}" is not a matroska file'.format(file_path))
        self._link_to_previous_options = ['--link-to-previous', '=' + file_path]

    def link_to_next(self, file_path):
        """Link the output file as the successor of the file_path file.

        file_path (str):
            Path of the file to be linked to.
        """
        # check if valid file
        if not isinstance(file_path, str):
            raise TypeError('"{}" is not of type str'.format(file_path))
        file_path = expanduser(file_path)
        if not MKVFile.verify_matroska(file_path):
            raise ValueError('"{}" is not a matroska file'.format(file_path))
        self._link_to_next_options = ['--link-to-next', '=' + file_path]

    @staticmethod
    def flatten(item):
        """Flatten a list.

        item (list, tuple):
            An iterable object with nested iterables to be flattened.
        """
        flat_list = []
        if isinstance(item, (list, tuple)):
            for item in item:
                flat_list.extend(MKVFile.flatten(item))
            return flat_list
        else:
            return [item]

    @staticmethod
    def verify_matroska(file_path, mkvmerge_path='mkvmerge'):
        """Verify a file is a Matroska file.

        file_path (str):
            Path of the file to be verified.
        mkvmerge_path (str):
            Alternate path to mkvmerge if it is not already in the $PATH variable.
        """
        if not isinstance(file_path, str):
            raise TypeError('"{}" is not of type str'.format(file_path))
        try:
            info_json = json.loads(sp.check_output([mkvmerge_path, '-J', expanduser(file_path)]).decode('utf8'))
        except sp.CalledProcessError:
            # TODO: refactor to raise error
            return False
        return info_json['container']['type'] == 'Matroska'
