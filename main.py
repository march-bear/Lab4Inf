from linpars import LinParsJSON, LinParsYAML
from conv import ConvToXML


def print_dict(format_dict, level):
    for key, value in format_dict.items():
        print('\t' * level + str(key), end=': ')
        if isinstance(value, dict):
            print()
            print_dict(value, level + 1)
        else:
            print(value)


def parse_json():
    try:
        with open(f"schedule.json", encoding="utf8") as schedule_file:
            format_code = schedule_file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("файл с расписанием не найден")

    try:
        python_format = LinParsJSON.read_elem(format_code, 0)[0]
    except Exception:
        raise Exception("ошибка конвертации в python-формат. Возможно, в файле schedule.json ошибка")

    return python_format


def parse_yml():
    try:
        with open("schedule.yml", encoding="utf8") as yaml_file:
            yaml_file_text = yaml_file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("файл с расписанием не найден")

    try:
        yaml_format = LinParsYAML.split_into_lines(LinParsYAML.del_comm(yaml_file_text))
    except Exception:
        raise Exception("ошибка конвертации в python-формат. Возможно, в файлу schedule.yaml ошибка")

    return LinParsJAML.read_elem(yaml_format, 0)[0]


def main():
    while True:
        try:
            print("Выберите формат (yml, json): ", end='')
            format_name = input()
            if format_name in ('yml', 'json'):
                break
            print("Повторите ввод: ", end='')
        except (EOFError, KeyboardInterrupt):
            print()
            print("Повторите ввод: ", end='')

    python_format = eval(f'parse_{format_name}()')

    print()
    print("Конвертация в python-формат прошла успешна. Форматированный вывод полученного формата: ", end='\n\n')
    for elem in python_format:
        print_dict(elem, 0)
        print()

    print()
    ConvToXML.write_format(python_format)
    print("Файл schedule.xml создан")


if __name__ == "__main__":
    main()
