# sheldon woodward
# 3/16/18

from re import match


class Timestamp:
    def __init__(self, timestamp=None, nn=None, ss=None, mm=None, hh=None, form='MM:SS'):
        self._hh = hh
        self._mm = mm
        self._ss = ss
        self._nn = nn
        self._form = form
        if timestamp is not None:
            self.extract(timestamp)
        else:
            self._hh = 0 if self._hh is None else self._hh
            self._mm = 0 if self._mm is None else self._mm
            self._ss = 0 if self._ss is None else self._ss
            self._nn = 0 if self._nn is None else self._nn

    @property
    def ts(self):
        # parse timestamp format
        format_groups = match('^(([Hh]{1,2}):)?([Mm]{1,2}):([Ss]{1,2})(\.([Nn]{1,9}))?$', self.form).groups()
        timestamp_format = [False if format_groups[i] is None else True for i in (1, 2, 3, 5)]

        # create timestamp string
        timestamp_string = ''
        if timestamp_format[0] or self._hh:
            timestamp_string += '{0:0=2d}:'.format(self.hh)
        if timestamp_format[1] or self._mm:
            timestamp_string += '{0:0=2d}:'.format(self.mm)
        if timestamp_format[2] or self._ss:
            timestamp_string += '{0:0=2d}'.format(self.ss)
        if timestamp_format[3] or self._nn:
            timestamp_string += '{:.9f}'.format(self.nn / 1000000000).rstrip('0')[1:] if self.nn else '.0'
        return timestamp_string

    @ts.setter
    def ts(self, timestamp):
        if not isinstance(timestamp, (int, str)):
            raise TypeError('"{}" is not str or int type'.format(type(timestamp)))
        else:
            self._hh = None
            self._mm = None
            self._ss = None
            self._nn = None
            self.extract(timestamp)

    @property
    def hh(self):
        return self._hh

    @hh.setter
    def hh(self, value):
        self._hh = value

    @property
    def mm(self):
        return self._mm

    @mm.setter
    def mm(self, value):
        self._mm = value if value < 60 else 0

    @property
    def ss(self):
        return self._ss

    @ss.setter
    def ss(self, value):
        self._ss = value if value < 60 else 0

    @property
    def nn(self):
        return self._nn

    @nn.setter
    def nn(self, value):
        self._nn = value if value < 1000000000 else 0

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, form):
        self._form = form

    @staticmethod
    def verify(timestamp):
        if not isinstance(timestamp, str):
            raise TypeError('"{}" is not str type'.format(type(timestamp)))
        elif match('^[0-9]{1,2}(:[0-9]{1,2}){1,2}(\.[0-9]{1,9})?$', timestamp):
            return True
        return False

    def extract(self, timestamp):
        if not isinstance(timestamp, (str, int)):
            raise TypeError('"{}" is not str or int type'.format(type(timestamp)))
        elif isinstance(timestamp, str) and not Timestamp.verify(timestamp):
            raise ValueError('"{}" is not a valid timestamp'.format(timestamp))
        elif isinstance(timestamp, str):
            # parse timestamp
            timestamp_groups = match('^(([0-9]{1,2}):)?([0-9]{1,2}):([0-9]{1,2})(\.([0-9]{1,9}))?$', timestamp).groups()
            timestamp = [timestamp_groups[i] for i in (1, 2, 3, 4)]
            timestamp_clean = []

            # clean timestamp
            for ts in timestamp:
                if ts is None:
                    timestamp_clean.append(0)
                else:
                    timestamp_clean.append(float(ts))

            # set timestamp variables
            self.hh = int(timestamp_clean[0]) if self._hh is None else self._hh
            self.mm = int(timestamp_clean[1]) if self._mm is None else self._mm
            self.ss = int(timestamp_clean[2]) if self._ss is None else self._ss
            self.nn = int(timestamp_clean[3] * 1000000000) if self._nn is None else self._nn

        elif isinstance(timestamp, int):
            self._hh = int(timestamp / 3600)
            self._mm = int(timestamp % 3600 / 60)
            self._ss = int(timestamp % 3600 % 60)
            self._nn = 0
