"""Abstract staganography class module

Copyright 2014 Maxim Syrykh
"""


class BaseSteganography:
    """Abstract staganography class"""
    def __init__(self, container):
        """Base init for staganography object"""
        self.container = container

    def encode(self):
        """Abstract encode method"""
        pass

    def decode(self):
        """Abstract decode method"""
        pass
