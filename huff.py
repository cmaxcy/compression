import heapq
from utils import Utils

class Huffman:

    @staticmethod
    def encode(text):
        text_char_dist = Utils.text_to_char_pmf(text)
        code = HuffTree.from_pmf(text_char_dist).code()
        return Utils.symbol_to_symbols_encode(text, code), code

    @staticmethod
    def decode(text, code):
        return Utils.symbols_to_symbol_decode(text, code)

class HuffTree:

    @staticmethod
    def from_pmf(pmf):
        q = [HuffTree(element, prob) for element, prob in pmf.items()]
        heapq.heapify(q)
        while len(q) > 1:
            lowest = heapq.heappop(q)
            second_lowest = heapq.heappop(q)
            merged = lowest.merge(second_lowest)
            heapq.heappush(q, merged)
        return q[0]

    def code(self):
        return self._code(self)

    @staticmethod
    def _code(tree):
        if tree is None:
            return dict()
        if tree.val is not None:
            return {tree.val: ''}

        left_code = HuffTree._code(tree.left)
        right_code = HuffTree._code(tree.right)

        code = dict()
        for element, encoding in left_code.items():
            code[element] = '1' + encoding
        for element, encoding in right_code.items():
            code[element] = '0' + encoding
        return code

    def __init__(self, val, weight):
        self.left = None
        self.right = None
        self.val = val
        self.weight = weight

    def __lt__(self, other):
        if self.weight == other.weight:
            if self.val is not None and other.val is not None:
                return self.val > other.val
        return self.weight < other.weight

    def __eq__(self, other):
        l = self.left == other.left
        r = self.right == other.right
        v = self.val == other.val
        w = self.weight == other.weight
        return l and r and v and w

    def merge(self, other):
        if other is None:
            raise ValueError('Merge attempted on empty tree')
        parent = HuffTree(None, self.weight + other.weight)
        if self < other:
            left, right = self, other
        else:
            left, right = other, self
        parent.left = left
        parent.right = right
        return parent
