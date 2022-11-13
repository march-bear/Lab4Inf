import re
from itertools import chain

arr_pattern = re.compile(r'(( )*- .*\n)', re.DOTALL)

class RegParsYAML:
    @staticmethod
    def read_obj():
        pass

    @staticmethod
    def read_arr():
        pass

    @staticmethod
    def read_elem():
        for i in chain():
            pass


if __name__ == "__main__":
    print(*arr_pattern.findall("- time:\n    - time_start: '8:20'\n    time_end: '9:50'\n- room:\n    - number:\nbuilding_address:"), sep='\n')