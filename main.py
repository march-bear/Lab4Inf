from linpars import LinParsYAML
from regpars import RegParsYAML
from conv import ConvToXML, ConvToCSV
from libparsconv import libConvXML, libParseYAML
import time


def conv_xml(python_format):
    if not python_format:
        print("Ни один из парсеров ещё не был запущен, формат не сформирован")
        return

    ConvToXML.write_format(python_format)
    print("Конвертация в XML прошла успешно")


def lib_conv_xml(python_format):
    if not python_format:
        print("Ни один из парсеров ещё не был запущен, формат не сформирован")
        return

    libConvXML(python_format)
    print("Конвертация в XML прошла успешно")


def conv_csv(python_format):
    if not python_format:
        print("Ни один из парсеров ещё не был запущен, формат не сформирован")
        return

    ConvToCSV.write_values(python_format)
    print("Конвертация в CSV прошла успешно")


def print_format(python_format):
    print(python_format)
    if not python_format:
        print("Ни один из парсеров ещё не был запущен, формат не сформирован")
        return

    def print_dict(format_dict, level):
        for key, value in format_dict.items():
            print('\t' * level + str(key), end=': ')
            if isinstance(value, dict):
                print()
                print_dict(value, level + 1)
            else:
                print(value)

    for elem in python_format:
        print_dict(elem, 0)
        print()


def reg_parse(yaml_format):
    try:
        python_format = RegParsYAML.read_arr(yaml_format)
        print("Конвертация в python-формат прошла успешно")
        return python_format
    except Exception:
        raise Exception("ошибка конвертации в python-формат. Возможно, в файлу schedule.yaml ошибка")


def lin_parse(yaml_file_text):
    try:
        yaml_format = LinParsYAML.split_into_lines(LinParsYAML.del_comm(yaml_file_text.strip()))
        python_format = LinParsYAML.read_elem(yaml_format, 0)[0]
        print("Конвертация в python-формат прошла успешно")
    except Exception:
        raise Exception("ошибка конвертации в python-формат. Возможно, в файлу schedule.yaml ошибка")
    return python_format


def analyze_runtime(yaml_file_text):
    print("Замер времени выполнения вызванного 100 раз парсера")

    python_format = yaml_file_text.strip()

    print("Линейный:\t\t\t\t\t\t", end='')
    start_time = time.time()
    for _ in range(100):
        lin_parse(python_format)
    print(time.time() - start_time)

    print("С регулярными выражениями:\t\t", end='')
    start_time = time.time()
    for _ in range(100):
        reg_parse(yaml_file_text)
    print(time.time() - start_time)

    print("С библиотеками:\t\t\t\t\t", end='')
    start_time = time.time()
    for _ in range(100):
        libParseYAML(yaml_file_text)
    print(time.time() - start_time)


def main():
    try:
        with open("schedule.yml", encoding="utf8") as yaml_file:
            yaml_file_text = yaml_file.read()
    except FileNotFoundError:
        raise FileNotFoundError("файл с расписанием не найден")

    print("q - выход\n"
          "1 - запустить линейный парсер\n"
          "2 - отобразить сформированный python-формат\n"
          "3 - запустить конвертацию в формат XML\n"
          "add1a - запустить парсер библиотеки pyyaml\n"
          "add1b - запустить конвертор библиотеки xml\n"
          "add2 - запустить парсер с регулярными выражениями\n"
          "add3 - запустить анализ времени работы парсеров\n"
          "add4 - запустить конвертацию в формат CSV\n"
          "\n"
          "Файл с расписанием прочитан, выберите команду: ", end='')

    while True:
        try:
            comm = input().strip()
            if comm == 'q':
                break
            elif comm == '1':
                python_format = lin_parse(yaml_file_text)
            elif comm == '2':
                print_format(python_format)
            elif comm == '3':
                conv_xml(python_format)
            elif comm == 'add1a':
                python_format = libParseYAML(yaml_file_text)
            elif comm == 'add1b':
                libConvXML(python_format)
            elif comm == 'add2':
                python_format = reg_parse(yaml_file_text)
            elif comm == 'add3':
                analyze_runtime(yaml_file_text)
            elif comm == 'add4':
                conv_csv(python_format)
            else:
                print("Команда не найдена")
            print()
            raise Exception
        except Exception as ex:
            print(ex)
            print("q - выход\n"
                  "1 - запустить линейный парсер\n"
                  "2 - отобразить сформированный python-формат\n"
                  "3 - запустить конвертацию в формат XML\n"
                  "add1a - запустить парсер библиотеки pyyaml\n"
                  "add1b - запустить конвертор библиотеки xml\n"
                  "add2 - запустить парсер с регулярными выражениями\n"
                  "add3 - запустить анализ времени работы парсеров\n"
                  "add4 - запустить конвертацию в формат CSV\n"
                  "\n"
                  "Выберите команду: ", end='')


if __name__ == "__main__":
    main()
