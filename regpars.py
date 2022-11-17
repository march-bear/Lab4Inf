import re


class RegParsYAML:
    comm_pattern = re.compile(r'#.*?\n')
    empty_line_pattern = re.compile(r'\n\s*\n')

    pair_pattern = re.compile(r'(\S+?): ?(.*)\n')
    obj_pattern = re.compile(r'(?:- | {2})((.+?):\n((?: {4}.+\n)*))')
    arr_pattern = re.compile(r'(( *)- .*?\n(?:\2( {2}).*?\n)*)', re.MULTILINE)
    num_pattern = re.compile(r'(^ *([\'\"])?-?[0-9]+(?:\.[0-9]+(?:[eE][0-9]+)?)?\2?)$', re.MULTILINE)

    @staticmethod
    def read_obj(src):
        obj = {}
        for elem in RegParsYAML.obj_pattern.findall(src):
            key = elem[1]
            value = {}
            for nested_key, nested_value in RegParsYAML.pair_pattern.findall(elem[2]):
                nested_value = nested_value.strip('\'\"')
                if RegParsYAML.num_pattern.search(nested_value):
                    value[nested_key] = eval(nested_value)
                else:
                    value[nested_key] = nested_value
            obj[key] = value
        src = RegParsYAML.obj_pattern.sub('', src)
        for elem in RegParsYAML.pair_pattern.findall(src):
            obj[elem[0]] = elem[1]
        return obj

    @staticmethod
    def read_arr(src):
        arr = []
        for elem in RegParsYAML.arr_pattern.findall(src):
            arr.append(RegParsYAML.read_obj(elem[0]))
        return arr


if __name__ == "__main__":
    try:
        with open("schedule.yml", encoding="utf8") as yaml_file:
            yaml_file_text = yaml_file.read()
    except FileNotFoundError:
        raise FileNotFoundError("файл с расписанием не найден")

    python_format = RegParsYAML.read_arr(yaml_file_text)
