# sheldon woodward
# 3/16/18

"""Timestamp Class"""

from re import match


class Timestamp:
    def __init__(self, timestamp=None, hh=None, mm=None, ss=None, nn=None, form='MM:SS'):
        """A class that represents a timestamp used in MKVFiles.

        The Timestamp class represents a timestamp used in mkvmerge. These are commonly used for splitting MKVFiles.
        Specific time values can overridden in the timestamp using 'hh', 'mm', 'ss', and 'nn'. Any override value
        that is greater than its maximum (ex. 61 minutes) will be set to 0.

        timestamp (str, int, Timestamp):
            A str of a timestamp acceptable to mkvmerge or an int representing seconds. This value will be
            the basis of the timestamp.
        hh (int):
            Hours in the timestamp. This will override the hours in the given timestamp.
        mm (int):
            Minutes in the timestamp. This will override the minutes in the given timestamp.
        ss (int):
            Seconds in the timestamp. This will override the seconds in the given timestamp.
        nn (int):
            Nanoseconds in the timestamp. This will override the nanoseconds in the given timestamp.
        form (int):
            A str for the form of the returned timestamp. 'MM' and 'SS' must be included where 'HH' and 'NN' are
            optional but will be included if 'hh' and 'nn' are not zero.
        """
        self._hh = hh
        self._mm = mm
        self._ss = ss
        self._nn = nn
        self._form = form
        if isinstance(timestamp, Timestamp):
            self._hh = timestamp.hh
            self._mm = timestamp.mm
            self._ss = timestamp.ss
            self._nn = timestamp.nn
        elif timestamp is not None:
            self.extract(timestamp)
        else:
            self._hh = 0 if self._hh is None else self._hh
            self._mm = 0 if self._mm is None else self._mm
            self._ss = 0 if self._ss is None else self._ss
            self._nn = 0 if self._nn is None else self._nn

    def __eq__(self, other):
        return self.hh == other.hh and self.mm == other.mm and self.ss == other.ss and self.nn == other.nn

    def __ne__(self, other):
        return self.hh != other.hh or self.mm != other.mm or self.ss != other.ss or self.nn != other.nn

    def __lt__(self, other):
        if self.hh != other.hh:
            return self.hh < other.hh
        elif self.mm != other.mm:
            return self.mm < other.mm
        elif self.ss != other.ss:
            return self.ss < other.ss
        elif self.nn != other.nn:
            return self.nn < other.nn
        return False

    def __le__(self, other):
        if self.hh != other.hh:
            return self.hh <= other.hh
        elif self.mm != other.mm:
            return self.mm <= other.mm
        elif self.ss != other.ss:
            return self.ss <= other.ss
        elif self.nn != other.nn:
            return self.nn <= other.nn
        return True

    def __gt__(self, other):
        if self.hh != other.hh:
            return self.hh > other.hh
        elif self.mm != other.mm:
            return self.mm > other.mm
        elif self.ss != other.ss:
            return self.ss > other.ss
        elif self.nn != other.nn:
            return self.nn > other.nn
        return False

    def __ge__(self, other):
        if self.hh != other.hh:
            return self.hh >= other.hh
        elif self.mm != other.mm:
            return self.mm >= other.mm
        elif self.ss != other.ss:
            return self.ss >= other.ss
        elif self.nn != other.nn:
            return self.nn >= other.nn
        return True

    def __str__(self):
        return self.ts

    def __getitem__(self, index):
        return (self.hh, self.mm, self.ss, self.ss)[index]

    @property
    def ts(self):
        """Generates the timestamp specified in the object."""
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
        """Set a new timestamp.

        timestamp (str, int):
            A str of a timestamp acceptable to mkvmerge or an int representing seconds. This value will be
            the basis of the timestamp.
        """
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
        """Verify a timestamp has the proper form to be used in mkvmerge.

        timestamp (str, int):
            The timestamp to be verified.
        """
        if not isinstance(timestamp, str):
            raise TypeError('"{}" is not str type'.format(type(timestamp)))
        elif match('^[0-9]{1,2}(:[0-9]{1,2}){1,2}(\.[0-9]{1,9})?$', timestamp):
            return True
        return False

    def extract(self, timestamp):
        """Extracts time info from a timestamp.

        timestamp (str, int):
            A str of a timestamp acceptable to mkvmerge or an int representing seconds. The timing info will be
            extracted from this parameter.
        """
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
