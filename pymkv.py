import subprocess as sp
import json


class Track:
    def __init__(self, path, codec=None, default_track=False, enabled_track=True, forced_track=False, language=None,
                 number=0, track_name=None, track_type=None, uid=None):
        self.path = path
        self.info_json = json.loads(sp.check_output(['mkvmerge', '-J', self.path]).decode('utf8'))
        self.info_string = json.dumps(self.info_json, indent=2)
        self.codec = codec
        self.default_track = default_track
        self.enabled_track = enabled_track
        self.forced_track = forced_track
        self.language = language
        self.number_original = number
        self.track_name = track_name
        self.track_type = track_type
        self.uid = uid


class File:
    def __init__(self, path):
        self.path = path
        self.info_json = json.loads(sp.check_output(['mkvmerge', '-J', self.path]).decode('utf8'))
        self.info_string = json.dumps(self.info_json, indent=2)
        self.title = None
        if 'title' in self.info_json['container']['properties']:
            self.title = self.info_json['container']['properties']['title']

        # add tracks with info
        self.tracks = []
        for track in self.info_json['tracks']:
            new_track = Track(path=self.path)
            if 'codec' in track:
                new_track.codec = track['codec']
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
            if 'type' in track:
                new_track.track_type = track['type']
            if 'uid' in track['properties']:
                new_track.uid = track['properties']['uid']
            self.tracks.append(new_track)

    def command(self, output_file, subprocess=False):
        command = ['mkvmerge', '-o', output_file]
        # universal attributes
        if self.title:
            command.extend(['--title', '"' + self.title + '"'])  # set title
        # add tracks
        for track in self.tracks:
            if track.track_name:
                command.extend(['--track-name', str(track.number_original) + ':"' + track.track_name + '"'])
            if track.language:
                command.extend(['--language', str(track.number_original) + ':' + track.language])
            if track.default_track:
                command.extend(['--default-track', str(track.number_original) + ':1'])
            if track.forced_track:
                command.extend(['--forced-track', str(track.number_original) + ':1'])
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
        print('Title: ' + self.title + '\n')
        for track in self.tracks:
            if track.codec is not None:
                print('Codec: ' + track.codec)
            if track.default_track is not None:
                print('Default Track: ' + str(track.default_track))
            if track.enabled_track is not None:
                print('Enabled Track: ' + str(track.enabled_track))
            if track.forced_track is not None:
                print('Forced Track: ' + str(track.forced_track))
            if track.language is not None:
                print('Language: ' + track.language)
            if track.number is not None:
                print('Number: ' + str(track.number))
            if track.track_name is not None:
                print('Track Name: ' + track.track_name)
            if track.track_type is not None:
                print('Track Type: ' + track.track_type)
            if track.uid is not None:
                print('UID: ' + str(track.uid) + '\n')

    def add_external_track(self, track):
        # single track
        self.tracks.append(track)


# class MKVObject:
#     # TODO: add optional track arguments
#     def __init__(self, output_file, title=None):
#         # initial values
#         self.output_file = output_file
#         self.title = title
#         self.tracks = []
#
#     # execution
#     def command(self, subprocess=False):
#         # setup command
#         command = ['mkvmerge', '-o', self.output_file]
#
#         # universal attributes
#         if self.title:
#             command.extend(['--title', self.title])  # set title
#
#         # add tracks
#         for track in self.tracks:
#             if track.title:
#                 command.extend(['--track-name', '0:' + track.title])
#             if track.language:
#                 command.extend(['--language', '0:' + track.language])
#             if track.default:
#                 command.extend(['--default-track', '0:1'])
#             if track.forced:
#                 command.extend(['--forced-track', '0:1'])
#             command.append(track.path)
#
#         if subprocess:
#             return command
#         return " ".join(command)
#
#     def mux(self):
#         command = self.command()
#         print('Running with command:\n"' + command + '"')
#         # TODO: add silent option to command execution
#         sp.run(self.command(subprocess=True))
#
#     # creation
#     def add_track(self, track):
#         if isinstance(track, Track):
#             self.tracks.append(track)
#         else:
#             print('Not a track')
#     #
#     # def add_file(self, file):
#     #     if isinstance(file, File):
#     #         for
