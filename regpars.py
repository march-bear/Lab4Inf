import re
from itertools import chain


class RegParsYAML:
    pair_pattern = re.compile(r'(.+): (.+)', re.DOTALL)
    obj_pattern = re.compile(r'', re.DOTALL)
    arr_pattern = re.compile(r'(?:- ())', re.DOTALL)
    num_pattern = re.compile(r'-?[0-9]+(?:.[0-9]+(?:[eE][0-9]+)?)?', re.DOTALL)
    str_pattern = re.compile(r'.+')

    @staticmethod
    def read_pair(src):
        pass

    @staticmethod
    def read_obj(src):
        pass

    @staticmethod
    def read_arr(src):
        pass

    @staticmethod
    def read_elem(src):
        for i in chain():
            pass


if __name__ == "__main__":
    pass
