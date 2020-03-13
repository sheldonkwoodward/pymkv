# sheldon woodward
# august 5, 2019

from pkg_resources import get_distribution, DistributionNotFound

# package imports
from .MKVAttachment import MKVAttachment
from .MKVTrack import MKVTrack
from .MKVFile import MKVFile
from .Timestamp import Timestamp
from .Verifications import verify_matroska, verify_mkvmerge, verify_recognized, verify_supported


# set the version number within the package using setuptools-scm
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = None
