import subprocess as sp
import json


class MKVTrack:
    def __init__(self, path, track_id=0, default_track=False, forced_track=False, language='eng', track_name=None):
        self.mkvmerge_path = 'mkvmerge'
        self.path = path
        self.default_track = default_track
        self.forced_track = forced_track
        self.language = language
        self.track_id = track_id
        self.track_name = track_name
        info_json = json.loads(sp.check_output([self.mkvmerge_path, '-J', self.path]).decode('utf8'))
        self.track_type = info_json['tracks'][track_id]['type']


class MKVFile:
    def __init__(self, path=None, title=None):
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
                new_track = MKVTrack(path=self.path, track_id=track['id'])
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
        if silent:
            sp.check_output(self.command(output_file, subprocess=True))
        else:
            command = self.command(output_file)
            print('Running with command:\n"' + command + '"')
            sp.run(self.command(output_file, subprocess=True))

    def add_track(self, track):
        self.tracks.append(track)

    def add_file(self, file):
        self.tracks = self.tracks + file.tracks

    def remove_track(self, track_num):
        if 0 <= track_num < len(self.tracks):
            del self.tracks[track_num]

    def move_track_front(self, track_num):
        if 0 <= track_num < len(self.tracks):
            self.tracks.insert(0, self.tracks.pop(self.tracks[track_num]))

    def move_track_end(self, track_num):
        if 0 <= track_num < len(self.tracks):
            self.tracks.append(self.tracks.pop(self.tracks[track_num]))

    def move_track_forward(self, track_num):
        if 0 <= track_num < len(self.tracks) - 1:
            self.tracks[track_num], self.tracks[track_num + 1] = self.tracks[track_num + 1], self.tracks[track_num]

    def move_track_backward(self, track_num):
        if 0 < track_num < len(self.tracks):
            self.tracks[track_num], self.tracks[track_num - 1] = self.tracks[track_num - 1], self.tracks[track_num]

    def swap_tracks(self, track_num_1, track_num_2):
        if 0 <= track_num_1 < len(self.tracks) and 0 <= track_num_2 < len(self.tracks):
            self.tracks[track_num_1], self.tracks[track_num_2] = self.tracks[track_num_2], self.tracks[track_num_1]
