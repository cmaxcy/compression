import unittest
import string
from LZ import LZ
from utils import Utils

class LZTest(unittest.TestCase):

    def test_encode_decode(self):
        encode_decode = lambda x: LZ.decode(LZ.encode(x))
        for _ in range(100):
            s = Utils.random_string(1000)
            self.assertEqual(encode_decode(s), s)

    def test_decode(self):
        sample_code = [(0, 'A'), (0, 'B'), (2, 'A'), (2, 'B'), (1, 'B'),
            (4, 'A'), (5, 'A'), (3, 'A')]
        expected_text = 'ABBABBABBBAABABAA'
        actual_text = LZ.decode(sample_code)
        self.assertEqual(expected_text, actual_text)

    def test_encode(self):
        sample_text = 'ABBABBABBBAABABAA'
        expected_encoding = [(0, 'A'), (0, 'B'), (2, 'A'), (2, 'B'), (1, 'B'),
            (4, 'A'), (5, 'A'), (3, 'A')]
        actual_encoding = LZ.encode(sample_text)
        self.assertEqual(expected_encoding, actual_encoding)

    def test_bits(self):
        f = lambda x: LZ.bits_to_code(LZ.code_to_bits(x))
        sample_code = [(0, 'A'), (0, 'B'), (2, 'A'), (2, 'B'), (1, 'B'),
            (4, 'A'), (5, 'A'), (3, 'A')]
        self.assertEqual(sample_code, f(sample_code))

    def test_encode_decode_bits(self):
        f = lambda x: LZ.decode(LZ.bits_to_code(LZ.code_to_bits(LZ.encode(x))))
        for _ in range(100):
            message = Utils.random_string(100)
            self.assertEqual(message, f(message))

if __name__ == '__main__':
    unittest.main()
