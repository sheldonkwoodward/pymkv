import subprocess as sp
import json


class Track:
    def __init__(self, path, default_track=False, enabled_track=True, forced_track=False, language='eng', number=0,
                 track_name=None):
        self.path = path
        self.default_track = default_track
        self.enabled_track = enabled_track
        self.forced_track = forced_track
        self.language = language
        self.number_original = number
        self.track_name = track_name


class File:
    def __init__(self, path=None):
        self.path = path
        self.title = None
        self.tracks = []
        if path:
            self.info_json = json.loads(sp.check_output(['mkvmerge', '-J', self.path]).decode('utf8'))
            self.info_string = json.dumps(self.info_json, indent=2)
            if 'title' in self.info_json['container']['properties']:
                self.title = self.info_json['container']['properties']['title']

            # add tracks with info
            for track in self.info_json['tracks']:
                new_track = Track(path=self.path)
                if 'default_track' in track['properties']:
                    new_track.default_track = track['properties']['default_track']
                if 'enabled_track' in track['properties']:
                    new_track.enabled_track = track['properties']['enabled_track']
                if 'forced_track' in track['properties']:
                    new_track.forced_track = track['properties']['forced_track']
                if 'language' in track['properties']:
                    new_track.language = track['properties']['language']
                if 'number' in track['properties']:
                    new_track.number_original = track['properties']['number'] - 1
                if 'track_name' in track['properties']:
                    new_track.track_name = track['properties']['track_name']
                self.add_track(new_track)

    def command(self, output_file, subprocess=False):
        command = ['mkvmerge', '-o', output_file]
        # universal attributes
        if self.title:
            command.extend(['--title', '"' + self.title + '"'])  # set title
        # add tracks
        for track_num, track in enumerate(self.tracks):
            if track.track_name:
                command.extend(['--track-name', str(track.number_original) + ':"' + track.track_name + '"'])
            if track.language:
                command.extend(['--language', str(track.number_original) + ':' + track.language])
            if not track.default_track:
                command.extend(['--default-track', str(track.number_original) + ':0'])
            if track.forced_track:
                command.extend(['--forced-track', str(track.number_original) + ':1'])
            try:
                if self.tracks[track_num + 1].path != track.path:
                    command.append(track.path)
            except IndexError:
                command.append(track.path)
        if subprocess:
            return command
        return " ".join(command)

    def mux(self, output_file):
        command = self.command(output_file)
        print('Running with command:\n"' + command + '"')
        # TODO: add silent option to command execution
        sp.run(self.command(output_file, subprocess=True))

    def print_info(self):
        if self.title:
            print('Title: ' + self.title + '\n')
        for track in self.tracks:
            print('\n')
            if track.default_track is not None:
                print('Default Track: ' + str(track.default_track))
            if track.enabled_track is not None:
                print('Enabled Track: ' + str(track.enabled_track))
            if track.forced_track is not None:
                print('Forced Track: ' + str(track.forced_track))
            if track.language is not None:
                print('Language: ' + track.language)
            if track.number_original is not None:
                print('Number: ' + str(track.number_original))
            if track.track_name is not None:
                print('Track Name: ' + track.track_name)

    def add_track(self, track):
        self.tracks.append(track)

    def add_file(self, file):
        self.tracks = self.tracks + file.tracks
