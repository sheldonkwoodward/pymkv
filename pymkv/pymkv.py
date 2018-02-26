# sheldon woodward
# 2/3/2018

import subprocess as sp
import json


class MKVTrack:
    def __init__(self, path, default_track=False, forced_track=False, language='eng', track_name=None):
        """An class that represents an MKV track such as video, audio, or subtitles.

        MKVTracks can be added to an MKVFile. MKVTracks can be video, audio, or subtitle tracks. The only required
        argument is path which gives the path to a track file.

        Args:
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
        self.mkvmerge_path = 'mkvmerge'
        self.path = path
        self.default_track = default_track
        self.forced_track = forced_track
        self.language = language
        self.track_id = 0
        self.track_name = track_name
        info_json = json.loads(sp.check_output([self.mkvmerge_path, '-J', self.path]).decode('utf8'))
        self.track_type = info_json['tracks'][self.track_id]['type']


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

        Args:
            path (str, optional):
                Path to a pre-existing MKV file. The file will be imported into the new MKVFile object.
            title (str, optional):
                The internal title given to the MKVFile. If no title is given, the title of the pre-existing file will be
                used if it exists.
        """
        self.mkvmerge_path = 'mkvmerge'
        self.path = path
        self.title = title
        self.tracks = []
        if path:
            # add file title
            info_json = json.loads(sp.check_output([self.mkvmerge_path, '-J', self.path]).decode('utf8'))
            if not self.title and 'title' in info_json['container']['properties']:
                self.title = info_json['container']['properties']['title']

            # add tracks with info
            for track in info_json['tracks']:
                new_track = MKVTrack(path=self.path)
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

        Args:
            output_file (str):
                The path to be used as the output file in the mkvmerge command.
            subprocess (bool):
                Will return the command as a list so it can be used easily with the subprocess module.

        Returns:
            Returns the command to create the specified MKV file. Return type is str by default. Will return as list if
            subprocess is true.
        """
        command = [self.mkvmerge_path, '-o', output_file]
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

            # add path
            command.append(track.path)

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
            sp.check_output(self.command(output_file, subprocess=True))
        else:
            command = self.command(output_file)
            print('Running with command:\n"' + command + '"')
            sp.run(self.command(output_file, subprocess=True))

    def add_track(self, track):
        """Add an MKVTrack to the MKVFile.

        track (MKVTrack):
            The MKVTrack to be added the MKVFile.
        """
        self.tracks.append(track)

    def add_file(self, file):
        """Combine an MKVFile with another MKVFile.

        file (MKVFile):
            The MKVFile to be combined with the MKVFile.
        """
        self.tracks = self.tracks + file.tracks

    def remove_track(self, track_num):
        """Remove a track from the MKVFile.

        track_num (int):
            The track number of the track to remove.
        """
        if 0 <= track_num < len(self.tracks):
            del self.tracks[track_num]
        else:
            raise IndexError('track index out of range')

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
