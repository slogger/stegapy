import unittest
import struct
import stegapy.errors
from stegapy.parsers.WAV import WAV


class TestRIFFWav(unittest.TestCase):
    def setUp(self):
        self.test_unit = WAV('test.wav')

    def test_params_read(self):
        _id = struct.unpack_from('>4s', self.test_unit.content[0:4])[0]
        self.assertEqual(_id, self.test_unit.chunk_id)

    def test_valid(self):
        self.assertTrue(self.test_unit.isValid())


class TestNotRIFFWav(unittest.TestCase):
    def test_valid(self):
        with self.assertRaises(stegapy.errors.ContainerError):
            WAV('test_not_riff.wav')

if __name__ == '__main__':
    unittest.main()
