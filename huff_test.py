import unittest
import os
import random
import string
from huff import HuffTree, Huffman
from utils import Utils

# TODO:
# - Consider making all tests non deterministic

class HuffTest(unittest.TestCase):

    def test_huffman_code_from_tree(self):
        # Create sample huffman tree
        sample_tree = HuffTree(None, 1)
        sample_tree.left = HuffTree('1', .4)
        sample_tree.right = HuffTree('2', .6)

        # Expected code
        expected_code = dict()
        expected_code['1'] = '1'
        expected_code['2'] = '0'

        actual_code = sample_tree.code()
        self.assertEqual(expected_code, actual_code)

    def test_huffman_tree_simple(self):
        # Create sample pmf
        sample_pmf = dict()
        sample_pmf['1'] = .4
        sample_pmf['2'] = .6

        # Expected huffman tree
        expected_tree = HuffTree(None, 1)
        expected_tree.left = HuffTree('1', .4)
        expected_tree.right = HuffTree('2', .6)

        actual_tree = HuffTree.from_pmf(sample_pmf)
        self.assertEqual(expected_tree, actual_tree)

    def test_HuffTree_lt(self):
        tree_1 = HuffTree('A', .5)
        tree_2 = HuffTree('A', .5)
        tree_3 = HuffTree('A', .6)
        tree_4 = HuffTree('B', .5)
        tree_5 = HuffTree('B', .6)

        self.assertFalse(tree_1 < tree_2)
        self.assertTrue(tree_1 < tree_3)
        self.assertFalse(tree_1 < tree_4)
        self.assertTrue(tree_4 < tree_1)

    def test_HuffTree_eq(self):
        tree_1 = HuffTree('A', .5)
        tree_2 = HuffTree('A', .5)
        tree_3 = HuffTree('A', .6)
        tree_4 = HuffTree('B', .5)
        tree_5 = HuffTree('B', .6)

        self.assertEqual(tree_1, tree_2)
        self.assertEqual(tree_2, tree_1)
        self.assertNotEqual(tree_1, tree_3)
        self.assertNotEqual(tree_3, tree_1)
        self.assertNotEqual(tree_1, tree_4)
        self.assertNotEqual(tree_1, tree_5)

    def test_merge_huff_tree_nodes_leaves(self):
        # Create sample leaf nodes
        node_1 = HuffTree('A', .4)
        node_2 = HuffTree('B', .6)

        expected_tree = HuffTree(None, 1)
        expected_tree.left = HuffTree('A', .4)
        expected_tree.right = HuffTree('B', .6)

        actual_tree = node_1.merge(node_2)
        self.assertEqual(expected_tree, actual_tree)

    def test_huffman(self):
        # Create sample pmf
        sample_pmf = dict()
        sample_pmf['1'] = .25
        sample_pmf['2'] = .25
        sample_pmf['3'] = .2
        sample_pmf['4'] = .15
        sample_pmf['5'] = .15

        # Create expected encoding
        expected_code = dict()
        expected_code['1'] = '01'
        expected_code['2'] = '10'
        expected_code['3'] = '11'
        expected_code['4'] = '000'
        expected_code['5'] = '001'

        actual_code = HuffTree.from_pmf(sample_pmf).code()
        self.assertEqual(expected_code, actual_code)

    def test_encode(self):
        # Create mock message and expected encoding
        message = '14235512213423211534'
        expected_encoding = '0100010110010010110100111000101110010100111000'
        actual_encoding, _ = Huffman.encode(message)

        self.assertEqual(expected_encoding, actual_encoding)

    def test_decode(self):
        # Create mock encoding and code
        encoding = '0100010110010010110100111000101110010100111000'
        code = dict()
        code['1'] = '01'
        code['2'] = '10'
        code['3'] = '11'
        code['4'] = '000'
        code['5'] = '001'

        # Create mock message and expected encoding
        expected_message = '14235512213423211534'
        actual_message = Huffman.decode(encoding, code)

        self.assertEqual(expected_message, actual_message)

    def test_encode_decode_id(self):
        for _ in range(100):
            message = Utils.random_string(100)
            message_pmf = Utils.text_to_char_pmf(message)
            encoding, code = Huffman.encode(message)
            decoding = Huffman.decode(encoding, code)
            self.assertEqual(message, decoding)

if __name__ == '__main__':
    unittest.main()
