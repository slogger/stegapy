"""Base container class module

Copyright 2014 Maxim Syrykh
"""


class BaseContainer:
    """Base class for container"""
    def __init__(self, name, read=False):
        """Base init"""
        self.name = name

    def read(self):
        """Abstract read method"""
        pass

    def write(self, content):
        """File write method"""
        with open(self.name, 'wb') as file:
            self.file_o = file
            if type(content) != bytes:
                content = bytes(content)
            self.file_o.write(content)

        return "OK"
