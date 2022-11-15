import re


class RegParsYAML:
    comm_pattern = re.compile(r'#.*?\n')
    empty_line_pattern = re.compile(r'\n\s*\n')

    pair_pattern = re.compile(r'(.+?): (.+)', re.MULTILINE)
    obj_pattern = re.compile(r'((.+?):\n(( +).+\n)*)', re.MULTILINE)
    arr_pattern = re.compile(r'(( *)- .*?\n(?:\2(- | {2}).*?\n)*)', re.MULTILINE)
    num_pattern = re.compile(r'(([\'\"])?-?[0-9]+(?:\.[0-9]+(?:[eE][0-9]+)?)?\2?)', re.MULTILINE)
    str_pattern = re.compile(r'.+')
    zero_level_pattern = re.compile(r'^.+\n', re.MULTILINE)

    @staticmethod
    def read_pair(src, curr_elem):
        pair = RegParsYAML.pair_pattern.match(src)
        if pair is None:
            return
        key, value = pair.group(1), RegParsYAML.read_elem(pair.group(2))
        if isinstance(curr_elem, list):
            curr_elem.append({key: value})
        else:
            curr_elem[key] = value
        return RegParsYAML.zero_level_pattern.sub('', src, 1)

    @staticmethod
    def read_obj(src):
        pass

    @staticmethod
    def read_arr(src):
        return RegParsYAML.arr_pattern.findall(src)

    @staticmethod
    def read_elem(src):
        pass


if __name__ == "__main__":
    try:
        with open("schedule.yml", encoding="utf8") as yaml_file:
            yaml_file_text = yaml_file.read()
    except FileNotFoundError:
        raise FileNotFoundError("файл с расписанием не найден")

    print(*RegParsYAML.read_arr(yaml_file_text), sep='\n')
