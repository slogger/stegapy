"""Module for parsing extra file

Copyright 2014 Maxim Syrykh
"""

from stegapy.models.container import BaseContainer
from stegapy.errors import InputError
from stegapy.errors import ContainerError
import gzip


class ExtraFile(BaseContainer):
    """Extra file class

    Fields:

        name – full filename
        content – binary data from file
        length – file size in bytes
    """

    def __init__(self, path):
        """Init method"""
        self.name = path
        # Try opening file
        try:
            with open(path, "rb") as f:
                self.content = gzip.compress(f.read())
        except FileNotFoundError:
            raise InputError("File not found")

        self.length = len(self.content)
        # If file is empty, throw exception
        if self.length == 0:
            raise InputError('File %s is empty!' % (self.name))

    def read(self):
        """Read method, return bytes data"""
        return self.content
