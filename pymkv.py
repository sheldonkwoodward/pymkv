import subprocess as sp


class Track:
    def __init__(self, path, title=None, language=None, default=None, forced=None):
        self.path = path
        self.title = title
        self.language = language
        self.default = default
        self.forced = forced


class VideoTrack(Track):
    def __init__(self, path, title=None, language=None, default=None, forced=None):
        super().__init__(path, title, language, default, forced)


class AudioTrack(Track):
    def __init__(self, path, title=None, language=None, default=None, forced=None):
        super().__init__(path, title, language, default, forced)


class SubtitleTrack(Track):
    def __init__(self, path, title=None, language=None, default=None, forced=None):
        super().__init__(path, title, language, default, forced)


class MKVObject:
    def __init__(self, output_file, title=None):
        # initial values
        self.output_file = output_file
        self.title = title
        self.tracks = []

    # execution
    def command(self):
        # setup command
        command = ['mkvmerge', '-o', self.output_file]

        # universal attributes
        if self.title:
            command.extend(['--title', self.title])  # set title

        # add tracks
        for track in self.tracks:
            if track.title:
                command.extend(['--track-name', '0:' + track.title])
            command.append(track.path)

        return command

    def mux(self):
        command = self.command()
        print('Running with command:\n"' + " ".join(command) + '"')
        sp.run(command)

    # creation
    def add_track(self, track):
        if isinstance(track, Track):
            self.tracks.append(track)
        else:
            print('Not a track')
