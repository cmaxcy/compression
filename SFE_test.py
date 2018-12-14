import unittest
# import pandas as pd
# from code import *
# import os
# import pygtrie
# import random
# import string
from SFE import SFE
from utils import Utils

class CodeTest(unittest.TestCase):

    def test_to_mod_cmf_to_code(self):
        self.assertEqual(SFE.mod_cmf_to_code(.125, 3), '001')
        self.assertEqual(SFE.mod_cmf_to_code(.5, 2), '10')
        self.assertEqual(SFE.mod_cmf_to_code(.8125, 4), '1101')
        self.assertEqual(SFE.mod_cmf_to_code(.9375, 4), '1111')

    def test_modified_cmf_from_pmf(self):
        # Create sample pmf
        sample_pmf = dict()
        sample_pmf['1'] = .25
        sample_pmf['2'] = .5
        sample_pmf['3'] = .125
        sample_pmf['4'] = .125

        # Expected modified cmf
        expected_modified_cmf = dict()
        expected_modified_cmf['1'] = .125
        expected_modified_cmf['2'] = .5
        expected_modified_cmf['3'] = .8125
        expected_modified_cmf['4'] = .9375

        actual_modified_cmf = SFE.modified_cmf_from_pmf(sample_pmf)
        self.assertEqual(expected_modified_cmf, actual_modified_cmf)

    def test_cmf_from_pmf(self):
        # Create sample pmf
        sample_pmf = dict()
        sample_pmf['1'] = .25
        sample_pmf['2'] = .5
        sample_pmf['3'] = .125
        sample_pmf['4'] = .125

        # Expected cmf
        expected_cmf = dict()
        expected_cmf['1'] = .25
        expected_cmf['2'] = .75
        expected_cmf['3'] = .875
        expected_cmf['4'] = 1.0

        actual_cmf = SFE.cmf_from_pmf(sample_pmf)
        self.assertEqual(expected_cmf, actual_cmf)

    def test_SFE_length(self):
        self.assertEqual(SFE.SFE_length(.25), 3)
        self.assertEqual(SFE.SFE_length(.5), 2)
        self.assertEqual(SFE.SFE_length(.125), 4)
        self.assertEqual(SFE.SFE_length(.125), 4)

    def test_SFE(self):
        # Create sample pmf
        sample_pmf = dict()
        sample_pmf['1'] = .25
        sample_pmf['2'] = .5
        sample_pmf['3'] = .125
        sample_pmf['4'] = .125

        # Create expected encoding
        expected_code = dict()
        expected_code['1'] = '001'
        expected_code['2'] = '10'
        expected_code['3'] = '1101'
        expected_code['4'] = '1111'

        actual_code = SFE.SFE(sample_pmf)
        self.assertEqual(expected_code, actual_code)

        # Create sample pmf
        sample_pmf = dict()
        sample_pmf['1'] = .25
        sample_pmf['2'] = .25
        sample_pmf['3'] = .2
        sample_pmf['4'] = .15
        sample_pmf['5'] = .15

        # Create expected encoding
        expected_code = dict()
        expected_code['1'] = '001'
        expected_code['2'] = '011'
        expected_code['3'] = '1001'
        expected_code['4'] = '1100'
        expected_code['5'] = '1110'

        actual_code = SFE.SFE(sample_pmf)
        self.assertEqual(expected_code, actual_code)

    def test_encode_decode(self):
        for _ in range(100):
            message = Utils.random_string(100)
            encoding, code = SFE.encode(message)
            decoding = SFE.decode(encoding, code)
            self.assertEqual(message, decoding)

if __name__ == '__main__':
    unittest.main()
