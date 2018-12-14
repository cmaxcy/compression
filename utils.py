import numpy as np
import pygtrie
import collections
import bitarray
import string
import random

class Utils:

    @staticmethod
    def random_string(length):
        # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def int_to_bits(i, bit_count=64):
        return bin(i)[2:].zfill(bit_count)

    @staticmethod
    def bits_to_int(bits):
        return int(bits, 2)

    @staticmethod
    def chunks(l, n):
        n = max(1, n)
        return (l[i:i+n] for i in range(0, len(l), n))

    @staticmethod
    def entropy(probs):
        return - np.dot(probs, np.log2(probs))

    @staticmethod
    def write_bits(bits, file_name):
        # https://stackoverflow.com/questions/6266330/python-bitarray-to-and-from-file
        ba = bitarray.bitarray(bits)
        with open(file_name, 'wb') as f:
            ba.tofile(f)

    @staticmethod
    def read_file(file_name):
        with open(file_name, 'r') as f:
            return f.read()

    @staticmethod
    def symbol_to_symbols_encode(text, code):
        f = lambda x: code[x]
        return ''.join(list(map(f, text)))

    @staticmethod
    def flip_dict(dictionary):
        # If dict values are not distinct
        if len(dictionary.values()) != len(set(dictionary.values())):
            raise ValueError('Dictionary values must be distinct')
        flipped_dict = dict()
        for key, item in dictionary.items():
            flipped_dict[item] = key
        return flipped_dict

    @staticmethod
    def symbols_to_symbol_decode(encoding, code):
        inverse_code = Utils.flip_dict(code)
        t = pygtrie.CharTrie()
        for code_word, value in inverse_code.items():
            t[code_word] = value
        decoding = []
        while encoding:
            next_decoded_word, value = t.longest_prefix(encoding)
            decoding.append(value)
            encoding = encoding[len(next_decoded_word):]
        return ''.join(decoding)

    @staticmethod
    def text_to_char_pmf(text):
        text_counts = collections.Counter(text)
        char_pmf = dict()
        total_chars = sum(text_counts.values())
        for char, count in text_counts.items():
            char_pmf[char] = count / total_chars
        return char_pmf
