import unittest
import random


class TestContainerModel(unittest.TestCase):
    def setUp(self):
        from stegapy.models.container import BaseContainer as container
        self.test_unit = container('test')

    def test_init(self):
        self.assertEqual(self.test_unit.name, 'test')

    def test_write(self):
        content = bytes(42)
        self.test_unit.write(content)
        with open('test', 'rb') as test_file:
            _file = test_file.read()
        self.assertEqual(_file, content)

    def test_write_two(self):
        content = 42
        self.test_unit.write(content)
        with open('test', 'rb') as test_file:
            _file = test_file.read()
        self.assertEqual(_file, bytes(content))


class TestStegtoolModel(unittest.TestCase):
    def setUp(self):
        from stegapy.models.stega import BaseSteganography
        self.stegtool = BaseSteganography
        self.num = random.Random()
        self.test_unit = self.stegtool(self.num)

    def test_container_setter(self):
        self.assertEqual(self.num, self.test_unit.container)

    def test_abstract_encode(self):
        self.assertEqual(None, self.test_unit.encode())

    def test_abstract_decode(self):
        self.assertEqual(None, self.test_unit.decode())


if __name__ == '__main__':
    unittest.main()
