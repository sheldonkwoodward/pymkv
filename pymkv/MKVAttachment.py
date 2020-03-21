""":class:`~pymkv.MKVAttachment` classes are used to represent attachment files within an MKV or to be used in an
MKV.

Examples
--------
Below are some basic examples of how the :class:`~pymkv.MKVAttachment` objects can be used.

Create a new :class:`~pymkv.MKVAttachment` and add it to an :class:`~pymkv.MKVFile`.

>>> from pymkv import MKVAttachment
>>> attachment = MKVAttachment('path/to/attachment.jpg', name='NAME')
>>> attachment.description = 'DESCRIPTION'

Attachments can also be added directly to an :class:`~pymkv.MKVFile`.

>>> from pymkv import MKVFile
>>> mkv = MKVFile('path/to/file.mkv')
>>> mkv.add_attachment('path/to/other/attachment.png')

Now, the MKV can be muxed with both attachments.

>>> mkv.add_attachment(attachment)
>>> mkv.mux('path/to/output.mkv')
"""

from os.path import expanduser, isfile
from mimetypes import guess_type


class MKVAttachment:
    """A class that represents an MKV attachment for an :class:`~pymkv.MKVFile` object.

    Parameters
    ----------
    file_path : str
        The path to the attachment file.
    name : str, optional
        The name that will be given to the attachment when muxed into a file.
    description : str, optional
        The description that will be given to the attachment when muxed into a file.
    attach_once : bool, optional
        Determines if the attachment should be added to all split files or only the first. Default is False,
        which will attach to all files.

    Attributes
    ----------
    mime_type : str
        The attachment's MIME type. The type will be guessed when :attr:`~pymkv.MKVAttachment.file_path` is set.
    name : str
        The name that will be given to the attachment when muxed into a file.
    description : str
        The description that will be given to the attachment when muxed into a file.
    attach_once : bool
        Determines if the attachment should be added to all split files or only the first. Default is False,
        which will attach to all files.
    """

    def __init__(self, file_path, name=None, description=None, attach_once=False):
        self.mime_type = None
        self._file_path = None
        self.file_path = file_path
        self.name = name
        self.description = description
        self.attach_once = attach_once

    def __repr__(self):
        return repr(self.__dict__)

    @property
    def file_path(self):
        """str: The path to the attachment file.

        Raises
        ------
        FileNotFoundError
            Raised if `file_path` does not exist.
        """
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        file_path = expanduser(file_path)
        if not isfile(file_path):
            raise FileNotFoundError('"{}" does not exist'.format(file_path))
        self.mime_type = guess_type(file_path)[0]
        self.name = None
        self._file_path = file_path
