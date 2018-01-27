import subprocess as sp


class Track:
    def __init__(self, path, title=None, language=None, default=False, forced=False):
        self.path = path
        self.title = title
        # TODO: check for valid language code
        self.language = language
        self.default = default
        self.forced = forced


class VideoTrack(Track):
    def __init__(self, path, title=None, language=None, default=False, forced=False):
        super().__init__(path, title, language, default, forced)


class AudioTrack(Track):
    def __init__(self, path, title=None, language=None, default=False, forced=False):
        super().__init__(path, title, language, default, forced)


class SubtitleTrack(Track):
    def __init__(self, path, title=None, language=None, default=False, forced=False):
        super().__init__(path, title, language, default, forced)


class MKVObject:
    # TODO: add optional track arguments
    def __init__(self, output_file, title=None):
        # initial values
        self.output_file = output_file
        self.title = title
        self.tracks = []

    # execution
    def command(self, subprocess=False):
        # setup command
        command = ['mkvmerge', '-o', self.output_file]

        # universal attributes
        if self.title:
            command.extend(['--title', self.title])  # set title

        # add tracks
        for track in self.tracks:
            if track.title:
                command.extend(['--track-name', '0:' + track.title])
            if track.language:
                command.extend(['--language', '0:' + track.language])
            if track.default:
                command.extend(['--default-track', '0:1'])
            if track.forced:
                command.extend(['--forced-track', '0:1'])
            command.append(track.path)

        if subprocess:
            return command
        return " ".join(command)

    def mux(self):
        command = self.command()
        print('Running with command:\n"' + " ".join(command) + '"')
        # TODO: add silent option to command exeecution
        sp.run(command)

    # creation
    def add_track(self, track):
        if isinstance(track, Track):
            self.tracks.append(track)
        else:
            print('Not a track')
