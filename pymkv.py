import subprocess as sp


# TODO: add default, forced, and language parameters
class Track:
    def __init__(self, path, title=None):
        self.path = path
        self.title = title


class VideoTrack(Track):
    def __init__(self, path, title=None):
        super().__init__(path, title)
        self.path = path
        self.title = title


class AudioTrack(Track):
    def __init__(self, path, title=None):
        super().__init__(path, title)
        self.path = path
        self.title = title


class SubtitleTrack(Track):
    def __init__(self, path, title=None):
        super().__init__(path, title)
        self.path = path
        self.title = title


class MKVObject:
    def __init__(self, output_file, title=None):
        # initial values
        self.command = []
        self.output_file = output_file
        self.title = title
        self.tracks = []

    def _build_command(self):
        # setup command
        self.command = ['mkvmerge', '-o', self.output_file]

        # universal attributes
        if self.title:
            self.command.extend(['--title', self.title])  # set title

        # add tracks
        for track in self.tracks:
            if track.title:
                self.command.extend(['--track-name', '0:' + track.title])
            self.command.append(track.path)

    def mux(self):
        self._build_command()
        print('Running with command:\n"' + " ".join(self.command) + '"')
        sp.run(self.command)

    def add_track(self, track):
        if isinstance(track, Track):
            self.tracks.append(track)
        else:
            print('Not a track')


movie = MKVObject('/Users/sheldonwoodward/Movies/test-project/output.mkv', 'MOVIE 1')
videoTrack = VideoTrack('/Users/sheldonwoodward/Movies/test-project/tracks/video.h264', 'VIDEO 1')
audioTrack1 = AudioTrack('/Users/sheldonwoodward/Movies/test-project/tracks/audio.aac', 'AUDIO 1')
audioTrack2 = AudioTrack('/Users/sheldonwoodward/Movies/test-project/tracks/audio.aac', 'AUDIO 2')

movie.add_track(videoTrack)
movie.add_track(audioTrack1)
movie.add_track(audioTrack2)
movie.mux()
