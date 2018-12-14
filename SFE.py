import numpy as np
from utils import Utils

# TODO:
# - make file name lower case
# - Improve naming of functions

class SFE:

    @staticmethod
    def encode(text):
        char_pmf = Utils.text_to_char_pmf(text)
        code = SFE.SFE(char_pmf)
        return Utils.symbol_to_symbols_encode(text, code), code

    @staticmethod
    def decode(message, code):
        return Utils.symbols_to_symbol_decode(message, code)

    @staticmethod
    def mod_cmf_to_code(mod_cmf, length):
        code = bin(int(mod_cmf * 2 ** length))[2:]
        while len(code) < length:
            code = '0' + code
        return code

    @staticmethod
    def modified_cmf_from_pmf(pmf):
        acc = 0
        cmf = dict()
        for element in sorted(pmf.keys()):
            cmf[element] = .5 * pmf[element] + acc
            acc += pmf[element]
        return cmf

    @staticmethod
    def cmf_from_pmf(pmf):
        acc = 0
        cmf = dict()
        for element in sorted(pmf.keys()):
            cmf[element] = pmf[element] + acc
            acc += pmf[element]
        return cmf

    @staticmethod
    def SFE_length(prob):
        return np.ceil(np.log2(1 / prob)) + 1

    @staticmethod
    def SFE(pmf):
        mod_cmf = SFE.modified_cmf_from_pmf(pmf)
        length = dict()
        for element, prob in pmf.items():
            length[element] = SFE.SFE_length(prob)

        code = dict()
        for element in mod_cmf:
            code[element] = SFE.mod_cmf_to_code(mod_cmf[element], length[element])

        return code
