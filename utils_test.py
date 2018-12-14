import unittest
import os
import random
import string
from utils import Utils
import bitarray

class UtilsTest(unittest.TestCase):

    def test_int_to_bits(self):
        self.assertEqual(Utils.int_to_bits(10, 5), '01010')

    def test_entropy(self):
        self.assertEqual(Utils.entropy([.5, .5]), 1)

    def setUp(self):
        # Create sample text file
        with open('test_file.txt', 'w') as f:
            f.write('Just\nSome\nSample\nText\n')

    def tearDown(self):
        # Delete sample text file
        if os.path.exists('test_file.txt'):
            os.remove('test_file.txt')
        if os.path.exists('sample_file.bin'):
            os.remove('sample_file.bin')

    def test_write_bits(self):
        sample_bits = '0111001011010100'
        sample_file = 'sample_file.bin'

        # Write bits to file
        Utils.write_bits(sample_bits, sample_file)

        # Read file back in
        expected_file_contents = bitarray.bitarray(sample_bits)
        actual_file_contents = bitarray.bitarray()
        with open(sample_file, 'rb') as f:
            actual_file_contents.fromfile(f)

        # Verify equality
        self.assertEqual(expected_file_contents, actual_file_contents)

    def test_read_file(self):
        expected_file_contents = 'Just\nSome\nSample\nText\n'
        actual_file_contents = Utils.read_file('test_file.txt')
        self.assertEqual(expected_file_contents, actual_file_contents)

    def test_symbol_by_symbol_encode(self):
        # Create mock code
        code = dict()
        code['1'] = '01'
        code['2'] = '10'
        code['3'] = '11'
        code['4'] = '000'
        code['5'] = '001'

        # Create mock message and expected encoding
        message = '452134'
        expected_encoding = '000001100111000'
        actual_encoding = Utils.symbol_to_symbols_encode(message, code)

        self.assertEqual(expected_encoding, actual_encoding)

    def test_symbol_by_symbol_decode(self):
        # Create mock code
        code = dict()
        code['1'] = '01'
        code['2'] = '10'
        code['3'] = '11'
        code['4'] = '000'
        code['5'] = '001'

        # Create mock message and expected encoding
        encoding = '000001100111000'
        expected_message = '452134'
        actual_message = Utils.symbols_to_symbol_decode(encoding, code)

        self.assertEqual(expected_message, actual_message)

    def test_int_and_bits(self):
        f = lambda x: Utils.bits_to_int(Utils.int_to_bits(x))
        for i in range(1000):
            self.assertEqual(i, f(i))

    def test_flip_dict(self):
        test_dict = {'a': 1, 'b': 2, 'c': 3}
        expected_flipped_dict = {1: 'a', 2: 'b', 3: 'c'}
        actual_flipped_dict = Utils.flip_dict(test_dict)
        self.assertEqual(expected_flipped_dict, actual_flipped_dict)

    def test_flip_dict_invalid(self):
        test_dict = {'a': 1, 'b': 1, 'c': 3}
        with self.assertRaises(ValueError):
            Utils.flip_dict(test_dict)

    def test_text_to_char_pmf(self):
        sample_text = 'aabc'
        expected_char_pmf = {'a': .5, 'b': .25, 'c': .25}
        actual_char_pmf = Utils.text_to_char_pmf(sample_text)
        self.assertEqual(expected_char_pmf, actual_char_pmf)

if __name__ == '__main__':
    unittest.main()
