# sheldon woodward
# 3/28/18

"""MKVAttachment Class"""

from os.path import expanduser, isfile
from mimetypes import guess_type


class MKVAttachment:
    def __init__(self, file_path, name=None, description=None):
        """A class that represents an MKV attachment.

        file_path (str):
            Path to a an attachment.
        name (str):
            The name of the attachment.
        description (str):
            The description of the attachment.
        """
        self._file_path = None
        self.file_path = file_path
        self._mime_type = None
        self.name = name
        self.description = description

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        file_path = expanduser(file_path)
        if not isfile(file_path):
            raise FileNotFoundError('"{}" does not exist'.format(file_path))
        self._mime_type = guess_type(file_path)[0]
        self.name = None
        self._file_path = file_path

    @property
    def mime_type(self):
        return self._mime_type
