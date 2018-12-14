from utils import Utils

class AdaptiveHuffman:

    @staticmethod
    def encode(text):
        tree = AdapHuffTree()
        return ''.join([tree.read_char(char) for char in text])

class AdapHuffNode:

    def __repr__(self):
        v = 'value: ' + str(self.val)
        w = 'weight: ' + str(self.weight)
        o = 'order: ' + str(self.order)
        return ', '.join([v, w, o])

    def __init__(self, val, weight, order, nyt, parent, left, right):
        self.val = val
        self.weight = weight
        self.order = order
        self.nyt = nyt
        self.parent = parent
        self.left = left
        self.right = right

    # TODO: consider how to handle parent comparison
    def __eq__(self, other):
        if other is None:
            return False
        l = self.left == other.left
        r = self.right == other.right
        v = self.val == other.val
        n = self.nyt == other.nyt
        w = self.weight == other.weight
        o = self.order == other.order
        return l and r and v and w and o and n

    def __ne__(self, other):
        return not self == other

class AdapHuffTree:

    def __init__(self):
        self.root = AdapHuffNode(val=None, weight=0, order=512, nyt=True,
            parent=None, left=None, right=None)

    def _weight_class(self, weight, node):
        if node is None:
            return []
        middle = []
        if node.weight == weight:
            middle.append(node)
        left = self._weight_class(weight, node.left)
        right = self._weight_class(weight, node.right)
        return left + middle + right

    def weight_class(self, weight):
        return self._weight_class(weight, self.root)

    def in_order(self):
        return self._in_order(self.root)

    def _in_order(self, node):
        if node is None:
            return []
        l = self._in_order(node.left)
        r = self._in_order(node.right)
        return l + [node] + r

    def to_root(self, node):
        if node.parent is None:
            return node
        return self.to_root(node.parent)

    def increment_weight(self, node):
        if node is None:
            return
        if node.parent is None:
            node.weight += 1
            return
        root = self.to_root(node)
        weight_class = self._weight_class(node.weight, root)
        max_order_node = max(weight_class, key=lambda x: x.order)
        if max_order_node != node.parent:
            self.swap(node, max_order_node)
        node.weight += 1
        self.increment_weight(node.parent)

    def swap(self, a, b):
        if a.parent is None:
            raise ValueError('Swap attempted on parent node')
        if b.parent is None:
            raise ValueError('Swap attempted on parent node')
        if a == b:
            return

        a_is_left = a.parent.left == a
        b_is_left = b.parent.left == b

        if a_is_left:
            if b_is_left:
                a.parent.left, b.parent.left = b.parent.left, a.parent.left
            else:
                a.parent.left, b.parent.right = b.parent.right, a.parent.left
        else:
            if b_is_left:
                a.parent.right, b.parent.left = b.parent.left, a.parent.right
            else:
                a.parent.right, b.parent.right = b.parent.right, a.parent.right

        a.parent, b.parent = b.parent, a.parent
        a.order, b.order = b.order, a.order

    def update_letter(self, letter):
        if self.find_letter(letter) == (None, None):
            raise ValueError('Letter does not exist')
        _, letter_node = self.find_letter(letter)
        self.increment_weight(letter_node)

    def add_letter(self, letter):
        if self.find_letter(letter) != (None, None):
            raise ValueError('Letter already exists')
        _, nyt = self.find_nyt()
        nyt.left = AdapHuffNode(val=None, weight=0, order=nyt.order - 2,
            nyt=True, parent=nyt, left=None, right=None)
        nyt.right = AdapHuffNode(val=letter, weight=0, order=nyt.order - 1,
            nyt=False, parent=nyt, left=None, right=None)
        nyt.nyt = False
        self.increment_weight(nyt.right)

    def _find_nyt(self, node):
        if node is None:
            return None, None
        if node.nyt:
            return '', node
        l_encoding, l_node = self._find_nyt(node.left)
        r_encoding, r_node = self._find_nyt(node.right)
        if l_encoding is not None:
            return '0' + l_encoding, l_node
        if r_encoding is not None:
            return '1' + r_encoding, r_node
        return None, None

    def find_nyt(self):
        return self._find_nyt(self.root)

    def find_letter(self, letter):
        return self._find_letter(letter, self.root)

    def _find_letter(self, letter, node):
        if node is None:
            return None, None
        if node.val == letter:
            return '', node

        l_encode, l_node = self._find_letter(letter, node.left)
        r_encode, r_node = self._find_letter(letter, node.right)

        if l_encode is not None:
            return '0' + l_encode, l_node
        if r_encode is not None:
            return '1' + r_encode, r_node
        return None, None

    def update_weights(self):
        return self._update_weights(self.root)

    def _update_weights(self, node):
        if node is None:
            return 0
        if node.val is not None:
            return node.weight

        l_weight = self._update_weights(node.left)
        r_weight = self._update_weights(node.right)
        total = l_weight + r_weight
        node.weight = total
        return total

    def read_char(self, char):
        letter_encoding, letter_leaf = self.find_letter(char)
        if letter_leaf is None:
            nyt_path, _ = self.find_nyt()
            self.add_letter(char)
            return nyt_path + Utils.int_to_bits(ord(char), bit_count=8)
        else:
            self.update_letter(char)
            return letter_encoding
