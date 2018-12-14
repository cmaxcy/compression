import unittest
from utils import Utils
from adap_huff import AdapHuffTree, AdapHuffNode, AdaptiveHuffman

class AdapHuffTest(unittest.TestCase):

    def setUp(self):
        # http://www2.cs.duke.edu/csed/curious/compression/eg5.html
        self.sample_tree = AdapHuffTree()

        root = AdapHuffNode(val=None, weight=4, order=512, nyt=False,
            parent=None, left=None, right=None)
        self.sample_tree.root = root

        l = AdapHuffNode(val=None, weight=2, order=510, nyt=False,
            parent=root, left=None, right=None)
        r = AdapHuffNode(val='a', weight=2, order=511, nyt=False,
            parent=root, left=None, right=None)
        root.left = l
        root.right = r

        ll = AdapHuffNode(val=None, weight=1, order=508, nyt=False,
             parent=l, left=None, right=None)
        lr = AdapHuffNode(val='r', weight=1, order=509, nyt=False,
             parent=l, left=None, right=None)
        l.left = ll
        l.right = lr

        lll = AdapHuffNode(val=None, weight=0, order=506, nyt=True,
              parent=ll, left=None, right=None)
        llr = AdapHuffNode(val='d', weight=1, order=507, nyt=False,
              parent=ll, left=None, right=None)
        ll.left = lll
        ll.right = llr

    def test_swap_root(self):
        with self.assertRaises(ValueError):
            self.sample_tree.swap(self.sample_tree.root, self.sample_tree.root.left)
        with self.assertRaises(ValueError):
            self.sample_tree.swap(self.sample_tree.root.right, self.sample_tree.root)
        self.sample_tree.swap(self.sample_tree.root.right, self.sample_tree.root.left)

    def test_swap_simple(self):

        actual_tree = AdapHuffTree()
        expected_root = AdapHuffNode(val=None, weight=0, order=512, nyt=True,
            parent=None, left=None, right=None)
        self.assertEqual(actual_tree.root, expected_root)

        # Read in a
        actual_tree.read_char('a')
        expected_root = AdapHuffNode(val=None, weight=1, order=512, nyt=False,
            parent=None, left=None, right=None)
        expected_root.left = AdapHuffNode(val=None, weight=0, order=510,
            nyt=True, parent=expected_root, left=None, right=None)
        expected_root.right = AdapHuffNode(val='a', weight=1, order=511,
            nyt=False, parent=expected_root, left=None, right=None)
        self.assertEqual(actual_tree.root, expected_root)

        actual_tree.swap(actual_tree.root.left, actual_tree.root.right)
        expected_root = AdapHuffNode(val=None, weight=1, order=512, nyt=False,
            parent=None, left=None, right=None)
        expected_root.right = AdapHuffNode(val=None, weight=0, order=511,
            nyt=True, parent=expected_root, left=None, right=None)
        expected_root.left = AdapHuffNode(val='a', weight=1, order=510,
            nyt=False, parent=expected_root, left=None, right=None)

        self.assertEqual(actual_tree.root, expected_root)

    def test_swap(self):

        pre_swap = AdapHuffTree()
        root = AdapHuffNode(val=None, weight=4, order=512, nyt=False,
            parent=None, left=None, right=None)
        pre_swap.root = root

        root.left = AdapHuffNode(val=None, weight=2, order=510, nyt=False,
            parent=root, left=None, right=None)
        root.right = AdapHuffNode(val='a', weight=2, order=511, nyt=False,
            parent=root, left=None, right=None)

        root.left.left = AdapHuffNode(val=None, weight=1, order=508, nyt=False,
             parent=root.left, left=None, right=None)
        root.left.right = AdapHuffNode(val='r', weight=1, order=509, nyt=False,
             parent=root.left, left=None, right=None)

        root.left.left.left = AdapHuffNode(val=None, weight=1, order=506,
            nyt=False, parent=root.left.left, left=None, right=None)
        root.left.left.right = AdapHuffNode(val='d', weight=1, order=507, nyt=False,
              parent=root.left.left, left=None, right=None)

        root.left.left.left.left = AdapHuffNode(val=None, weight=0, order=504,
            nyt=True, parent=root.left.left.left, left=None, right=None)
        root.left.left.left.right = AdapHuffNode(val='v', weight=1, order=505,
            nyt=False, parent=root.left.left.left, left=None, right=None)

        expected_post_swap = AdapHuffTree()
        root = AdapHuffNode(val=None, weight=4, order=512, nyt=False,
            parent=None, left=None, right=None)
        expected_post_swap.root = root

        root.left = AdapHuffNode(val=None, weight=2, order=510, nyt=False,
            parent=root, left=None, right=None)
        root.right = AdapHuffNode(val='a', weight=2, order=511, nyt=False,
            parent=root, left=None, right=None)

        root.left.right = AdapHuffNode(val=None, weight=1, order=509, nyt=False,
             parent=root.left, left=None, right=None)
        root.left.left = AdapHuffNode(val='r', weight=1, order=508, nyt=False,
             parent=root.left, left=None, right=None)

        root.left.right.left = AdapHuffNode(val=None, weight=1, order=506,
            nyt=False, parent=root.left.right, left=None, right=None)
        root.left.right.right = AdapHuffNode(val='d', weight=1, order=507, nyt=False,
              parent=root.left.right, left=None, right=None)

        root.left.right.left.left = AdapHuffNode(val=None, weight=0, order=504,
            nyt=True, parent=root.left.right.left, left=None, right=None)
        root.left.right.left.right = AdapHuffNode(val='v', weight=1, order=505,
            nyt=False, parent=root.left.right.left, left=None, right=None)

        pre_swap.swap(pre_swap.root.left.left, pre_swap.root.left.right)
        self.assertEqual(pre_swap.root, expected_post_swap.root)

    def test_find_nyt(self):
        expected_encoding = '000'
        expected_node = self.sample_tree.root.left.left.left
        actual_encoding, actual_node = self.sample_tree.find_nyt()
        self.assertEqual(expected_encoding, actual_encoding)
        self.assertEqual(expected_node, actual_node)

    def test_update_weights(self):

        # Verify root can have weight updated
        self.assertEqual(self.sample_tree.root.weight, 4)
        self.sample_tree.root.weight = 0
        self.assertEqual(self.sample_tree.root.weight, 0)
        self.assertEqual(self.sample_tree.update_weights(), 4)
        self.assertEqual(self.sample_tree.root.weight, 4)

    def test_find_letter(self):

        # Find a
        expected_encoding = '1'
        expected_node = self.sample_tree.root.right
        actual_encoding, actual_node = self.sample_tree.find_letter('a')
        self.assertEqual(expected_encoding, actual_encoding)
        self.assertEqual(expected_node, actual_node)

        # Find r
        expected_encoding = '01'
        expected_node = self.sample_tree.root.left.right
        actual_encoding, actual_node = self.sample_tree.find_letter('r')
        self.assertEqual(expected_encoding, actual_encoding)
        self.assertEqual(expected_node, actual_node)

        # Find d
        expected_encoding = '001'
        expected_node = self.sample_tree.root.left.left.right
        actual_encoding, actual_node = self.sample_tree.find_letter('d')
        self.assertEqual(expected_encoding, actual_encoding)
        self.assertEqual(expected_node, actual_node)

        # Find h
        expected_encoding = None
        expected_node = None
        actual_encoding, actual_node = self.sample_tree.find_letter('h')
        self.assertEqual(expected_encoding, actual_encoding)
        self.assertEqual(expected_node, actual_node)

    def test_encode_large(self):
        actual_tree = AdapHuffTree()
        for char in 'astrachan ':
            actual_tree.read_char(char)

        expected_root = AdapHuffNode(val=None, weight=10, order=512, nyt=False,
            parent=None, left=None, right=None)

        expected_root.left = AdapHuffNode(val=None, weight=4, order=510,
            nyt=False, parent=expected_root, left=None, right=None)
        expected_root.right = AdapHuffNode(val=None, weight=6, order=511,
            nyt=False, parent=expected_root, left=None, right=None)

        expected_root.left.left = AdapHuffNode(val=None, weight=2, order=506,
            nyt=False, parent=expected_root.left, left=None, right=None)
        expected_root.left.right = AdapHuffNode(val=None, weight=2, order=507,
            nyt=False, parent=expected_root.left, left=None, right=None)
        expected_root.right.left = AdapHuffNode(val=None, weight=3, order=508,
            nyt=False, parent=expected_root.right, left=None, right=None)
        expected_root.right.right = AdapHuffNode(val='a', weight=3, order=509,
            nyt=False, parent=expected_root.right, left=None, right=None)
        expected_root.left.left.left = AdapHuffNode(val='r', weight=1, order=500,
            nyt=False, parent=expected_root.left.left, left=None, right=None)
        expected_root.left.left.right = AdapHuffNode(val='h', weight=1, order=501,
            nyt=False, parent=expected_root.left.left, left=None, right=None)
        expected_root.left.right.left = AdapHuffNode(val='s', weight=1, order=502,
            nyt=False, parent=expected_root.left.right, left=None, right=None)
        expected_root.left.right.right = AdapHuffNode(val='c', weight=1, order=503,
            nyt=False, parent=expected_root.left.right, left=None, right=None)
        expected_root.right.left.left = AdapHuffNode(val='t', weight=1, order=504,
            nyt=False, parent=expected_root.right.left, left=None, right=None)
        expected_root.right.left.right = AdapHuffNode(val=None, weight=2, order=505,
            nyt=False, parent=expected_root.right.left, left=None, right=None)

        expected_root.right.left.right.left = AdapHuffNode(val=None, weight=1,
            order=498, nyt=False, parent=expected_root.right.left.right,
            left=None, right=None)
        expected_root.right.left.right.right = AdapHuffNode(val='n', weight=1,
            order=499, nyt=False, parent=expected_root.right.left.right,
            left=None, right=None)

        expected_root.right.left.right.left.left = AdapHuffNode(val=None,
            weight=0, order=496, nyt=True,
            parent=expected_root.right.left.right.left, left=None, right=None)
        expected_root.right.left.right.left.right = AdapHuffNode(val=' ',
            weight=1, order=497, nyt=False,
            parent=expected_root.right.left.right.left, left=None, right=None)

        self.assertEqual(actual_tree.root, expected_root)

    def test_encode_code_matches(self):
        tree = AdapHuffTree()

        char_to_bits = lambda c: Utils.int_to_bits(ord(c), bit_count=8)

        expected_code = char_to_bits('a')
        actual_code = tree.read_char('a')
        self.assertEqual(expected_code, actual_code)

        expected_code = '1'
        actual_code = tree.read_char('a')
        self.assertEqual(expected_code, actual_code)

        expected_code = '0' + char_to_bits('r')
        actual_code = tree.read_char('r')
        self.assertEqual(expected_code, actual_code)

        expected_code = '00' + char_to_bits('d')
        actual_code = tree.read_char('d')
        self.assertEqual(expected_code, actual_code)

        expected_code = '000' + char_to_bits('v')
        actual_code = tree.read_char('v')
        self.assertEqual(expected_code, actual_code)

    def test_encode(self):
        text = 'aardv'
        expected_code = '011000011001110010000110010000001110110'
        actual_code = AdaptiveHuffman.encode(text)
        self.assertEqual(expected_code, actual_code)

    def test_encode_tree_matches(self):

        actual_tree = AdapHuffTree()
        expected_root = AdapHuffNode(val=None, weight=0, order=512, nyt=True,
            parent=None, left=None, right=None)
        self.assertEqual(actual_tree.root, expected_root)

        # Read in a
        actual_tree.read_char('a')
        expected_root = AdapHuffNode(val=None, weight=1, order=512, nyt=False,
            parent=None, left=None, right=None)
        expected_root.left = AdapHuffNode(val=None, weight=0, order=510,
            nyt=True, parent=expected_root, left=None, right=None)
        expected_root.right = AdapHuffNode(val='a', weight=1, order=511,
            nyt=False, parent=expected_root, left=None, right=None)
        self.assertEqual(actual_tree.root, expected_root)

        # Read in a
        actual_tree.read_char('a')
        expected_root = AdapHuffNode(val=None, weight=2, order=512, nyt=False,
            parent=None, left=None, right=None)
        expected_root.left = AdapHuffNode(val=None, weight=0, order=510,
            nyt=True, parent=expected_root, left=None, right=None)
        expected_root.right = AdapHuffNode(val='a', weight=2, order=511,
            nyt=False, parent=expected_root, left=None, right=None)
        self.assertEqual(actual_tree.root, expected_root)

        # Read in r
        actual_tree.read_char('r')
        expected_root = AdapHuffNode(val=None, weight=3, order=512, nyt=False,
            parent=None, left=None, right=None)
        expected_root.left = AdapHuffNode(val=None, weight=1, order=510,
            nyt=False, parent=expected_root, left=None, right=None)
        expected_root.right = AdapHuffNode(val='a', weight=2, order=511,
            nyt=False, parent=expected_root, left=None, right=None)
        expected_root.left.left = AdapHuffNode(val=None, weight=0, order=508,
            nyt=True, parent=expected_root.left, left=None, right=None)
        expected_root.left.right = AdapHuffNode(val='r', weight=1, order=509,
            nyt=False, parent=expected_root.left, left=None, right=None)
        self.assertEqual(actual_tree.root, expected_root)

        # Read in d
        actual_tree.read_char('d')
        expected_root = AdapHuffNode(val=None, weight=4, order=512, nyt=False,
            parent=None, left=None, right=None)
        expected_root.left = AdapHuffNode(val=None, weight=2, order=510,
            nyt=False, parent=expected_root, left=None, right=None)
        expected_root.right = AdapHuffNode(val='a', weight=2, order=511,
            nyt=False, parent=expected_root, left=None, right=None)
        expected_root.left.left = AdapHuffNode(val=None, weight=1, order=508,
            nyt=False, parent=expected_root.left, left=None, right=None)
        expected_root.left.right = AdapHuffNode(val='r', weight=1, order=509,
            nyt=False, parent=expected_root.left, left=None, right=None)
        expected_root.left.left.left = AdapHuffNode(val=None, weight=0,
            order=506, nyt=True, parent=expected_root.left.left, left=None,
            right=None)
        expected_root.left.left.right = AdapHuffNode(val='d', weight=1,
            order=507, nyt=False, parent=expected_root.left.left, left=None,
            right=None)
        self.assertEqual(actual_tree.root, expected_root)

        # Read in v
        actual_tree.read_char('v')
        expected_root = AdapHuffNode(val=None, weight=5, order=512, nyt=False,
            parent=None, left=None, right=None)
        expected_root.left = AdapHuffNode(val='a', weight=2, order=510,
            nyt=False, parent=expected_root, left=None, right=None)
        expected_root.right = AdapHuffNode(val=None, weight=3, order=511,
            nyt=False, parent=expected_root, left=None, right=None)
        expected_root.right.left = AdapHuffNode(val='r', weight=1, order=508,
            nyt=False, parent=expected_root.right, left=None, right=None)
        expected_root.right.right = AdapHuffNode(val=None, weight=2, order=509,
            nyt=False, parent=expected_root.right, left=None, right=None)
        expected_root.right.right.left = AdapHuffNode(val=None, weight=1,
            order=506, nyt=False, parent=expected_root.right.right, left=None,
            right=None)
        expected_root.right.right.right = AdapHuffNode(val='d', weight=1,
            order=507, nyt=False, parent=expected_root.right.right, left=None,
            right=None)
        expected_root.right.right.left.left = AdapHuffNode(val=None, weight=0,
            order=504, nyt=True, parent=expected_root.right.right.left,
            left=None, right=None)
        expected_root.right.right.left.right = AdapHuffNode(val='v', weight=1,
            order=505, nyt=False, parent=expected_root.right.right.left,
            left=None, right=None)

        self.assertEqual(actual_tree.root, expected_root)

    def test_weight_class(self):
        # Weight class of 1
        expected_weight_class = [self.sample_tree.root.left.left,
            self.sample_tree.root.left.left.right,
            self.sample_tree.root.left.right]
        actual_weight_class = self.sample_tree.weight_class(1)
        self.assertEqual(expected_weight_class, actual_weight_class)

        # Weight class of 2
        expected_weight_class = [self.sample_tree.root.left,
            self.sample_tree.root.right]
        actual_weight_class = self.sample_tree.weight_class(2)
        self.assertEqual(expected_weight_class, actual_weight_class)

    def test_huff_node_eq(self):
        self.assertEqual(AdapHuffNode(None, 0, 512, False, None, None, None),
            AdapHuffNode(None, 0, 512, False, None, None, None))
        self.assertNotEqual(AdapHuffNode(None, 0, 512, False, None, None, None),
            AdapHuffNode(None, 0, 512, True, None, None, None))
        self.assertNotEqual(AdapHuffNode(12, 0, 512, False, None, None, None),
            AdapHuffNode(None, 0, 512, False, None, None, None))

if __name__ == '__main__':
    unittest.main()
