# sheldon woodward
# august 5, 2019

from pkg_resources import get_distribution, DistributionNotFound

from .MKVAttachment import *
from .MKVTrack import *
from .MKVFile import *
from .Timestamp import *
from .Verifications import *


# set the version number within the package using setuptools-scm
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = None