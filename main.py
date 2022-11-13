from linpars import LinParsJSON, LinParsJAML
from conv import ConvToXML
import json


def print_dict(format_dict, level):
    for key, value in format_dict.items():
        print('\t' * level + str(key), end=': ')
        if isinstance(value, dict):
            print()
            print_dict(value, level + 1)
        else:
            print(value)


def main():
    try:
        with open("schedule.json", encoding="utf8") as json_file:
            json_format = json_file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("файл с расписанием не найден")

    try:
        python_format = LinParsJSON.read_elem(json_format, 0)[0]
    except Exception:
        raise Exception("ошибка конвертации в python-формат. Возможно в файле schedule.json ошибка")

    for elem in python_format:
        print_dict(elem, 0)

    python_format_standard = json.loads(json_format)
    print(python_format_standard)

    ConvToXML.write_format(python_format)


if __name__ == "__main__":
    # main()
    try:
        with open("schedule.yml", encoding="utf8") as yaml_file:
            yaml_file_text = yaml_file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("файл с расписанием не найден")
    yaml_format = LinParsJAML.split_into_lines(LinParsJAML.del_comm(yaml_file_text))
    print(yaml_format)
    python_format = LinParsJAML.read_elem(yaml_format, 0)[0]
    print(python_format)
    for i in python_format:
        print_dict(i, 0)
    ConvToXML.write_format(python_format)
