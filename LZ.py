import pygtrie
import collections
from utils import Utils

class LZ:

    @staticmethod
    def bits_to_code(bits, bit_count=16):
        bit_chunks = Utils.chunks(bits, bit_count + 8)
        code = []
        for bit_chunk in bit_chunks:
            count_bits, char_bits = bit_chunk[:bit_count], bit_chunk[bit_count:]
            count = Utils.bits_to_int(count_bits)
            if not char_bits:
                char = ''
            else:
                char = chr(Utils.bits_to_int(char_bits))
            code.append((count, char))
        return code

    @staticmethod
    def code_to_bits(code, bit_count=16):
        bits = []
        for count, char in code:
            count_bits = Utils.int_to_bits(count, bit_count=bit_count)
            if char == '':
                char_bits = ''
            else:
                char_bits = Utils.int_to_bits(ord(char), bit_count=8)
            bits.append(count_bits)
            bits.append(char_bits)
        return ''.join(bits)

    @staticmethod
    def _decode(code, pair, cache):
        if pair in cache:
            return cache[pair]

        index, char = pair
        if index == 0:
            cache[pair] = char
            return char
        next_pair = code[index - 1]
        word = LZ._decode(code, next_pair, cache) + char
        cache[pair] = word
        return word

    @staticmethod
    def decode(code):
        cache = dict()
        return ''.join([LZ._decode(code, pair, cache) for pair in code])

    @staticmethod
    def encode(text):
        code = []
        t = pygtrie.CharTrie()
        i = 0
        while i < len(text):
            suffix = text[i:]
            longest_prefix = t.longest_prefix(suffix)
            if not longest_prefix:
                code.append((0, text[i]))
                t[text[i]] = len(code)
                i += 1
            else:
                prefix, location = longest_prefix
                if i + len(prefix) == len(text):
                    new_char = ''
                else:
                    new_char = text[i + len(prefix)]
                code.append((location, new_char))
                t[prefix + new_char] = len(code)
                i += len(prefix) + 1
        return code

    @staticmethod
    def bit_encode(text):
        return LZ.code_to_bits(LZ.encode(text))
