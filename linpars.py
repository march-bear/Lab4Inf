class LinParsJSON:
    @staticmethod
    def read_word(text, index):
        i = index
        word = ''

        while i < len(text) and text[i] != '\"':
            word += text[i]
            i += 1

        return word, i

    @staticmethod
    def read_literal(text, index):
        text_i = text[index]

        if text_i == 't':
            return True, index + 3
        elif text_i == 'f':
            return False, index + 4
        return None, index + 3

    @staticmethod
    def read_num(text, index):
        i = index
        num = ''

        while i < len(text) and (text[i] in '.-' or text[i].isdigit()):
            num += text[i]
            i += 1

        i -= 1
        return int(num) if num.isdigit() else float(num), i

    @staticmethod
    def read_arr(text, index):
        i = index
        arr = []

        while text[i] != ']':
            if text[i] in ('\"', '[', '{', '-') or text[i] in 'ftn' or text[i].isdigit():
                elem, i = LinParsJSON.read_elem(text, i)
                arr.append(elem)
            i += 1

        return arr, i

    @staticmethod
    def read_obj(text, index):
        i = index
        obj = dict()

        while text[i] != '}':
            if text[i] == '\"':
                key, i = LinParsJSON.read_word(text, i + 1)
                i += 1
                while not (text[i] in ('\"', '[', '{', '-') or text[i] in 'ftn' or text[i].isdigit()):
                    i += 1
                value, i = LinParsJSON.read_elem(text, i)
                obj[key] = value
            i += 1
        return obj, i

    @staticmethod
    def read_elem(text, index):
        if text[index] == '\"':
            return LinParsJSON.read_word(text, index + 1)
        elif text[index] == '{':
            return LinParsJSON.read_obj(text, index + 1)
        elif text[index] == '[':
            return LinParsJSON.read_arr(text, index + 1)
        elif text[index] == '-' or text[index].isdigit():
            return LinParsJSON.read_num(text, index)
        else:
            return LinParsJSON.read_literal(text, index)


class LinParsJAML:
    @staticmethod
    def del_comm(text):
        stack = ''
        i = 0

        while i < len(text):
            if text[i] in ('"', "'"):
                if not stack:
                    stack = text[i]
                elif stack == text[i]:
                    stack = ''
            elif text[i] == '#' and not stack:
                j = i + 1
                while text[j] != '\n':
                    j += 1
                text = text[:i] + text[j:]
            i += 1
        return text

    @staticmethod
    def remove_quotes(string):
        if string[0] == string[-1] and string[0] in '\'\"':
            return string[1:-1]
        return string

    @staticmethod
    def to_number(string):
        try:
            n1 = int(string)
            n2 = float(string)
        except ValueError:
            return string
        if n1 == n2:
            return n1
        return n2

    @staticmethod
    def to_literal(string):
        if string == "true":
            return True
        elif string == "false":
            return False
        elif string == "":
            return None
        return string

    @staticmethod
    def split_into_lines(text):
        text = text.split('\n')
        i = 0

        while i < len(text):
            if text[i] in ('', '---'):
                del text[i]
            else:
                string = text[i].lstrip(' ').rstrip()
                text[i] = [string, (len(text[i]) - len(string.lstrip('-'))) // 2]
                i += 1

        return text

    @staticmethod
    def separating_colon(string):
        if ': ' in string:
            i = 0
            stack = ''

            while i < len(string) - 1:
                if string[i] in ('"', "'"):
                    if not stack:
                        stack = string[i]
                    elif stack == string[i]:
                        stack = ''
                elif (string[i] + string[i + 1] == ': ') and not stack:
                    return True
                i += 1
        return False

    @staticmethod
    def read_dict(text, index):
        dict_ = dict()

        i = index
        level_dict = text[index][1]

        while i < len(text) and text[i][1] >= level_dict and text[i][0][0] != '-':
            if text[i][0][-1] == ':':
                key = LinParsJAML.remove_quotes(text[i][0][:-1])
                if i < len(text):
                    if text[i + 1][1] <= level_dict and text[i + 1][0] != '-':
                        value = None
                        i += 1
                    else:
                        value, i = LinParsJAML.read_elem(text, i + 1)
                else:
                    value = None
                    i += 1
            else:
                key, value = map(LinParsJAML.remove_quotes, text[i][0].split(': ', 1))

                if isinstance(value, str):
                    value, _ = LinParsJAML.read_string([(value,)], 0)

                i += 1
            dict_[key] = value

        return dict_, i

    @staticmethod
    def read_arr(text, index):
        arr = []

        i = index
        level_arr = text[index][1]

        while i < len(text) and text[i][1] >= level_arr:
            text[i][0] = text[i][0].lstrip('- ')
            if text[i][0] == '' and not text[i + 1][0].startswith('-'):
                if i + 1 < len(text):
                    if text[i + 1][1] > level_arr:
                        i += 1
                    else:
                        elem = None
                        arr.append(elem)
                        i += 1
                        break
                else:
                    elem = None
                    arr.append(elem)
                    i += 1
                    break
            elem, i = LinParsJAML.read_elem(text, i)
            if isinstance(elem, str):
                elem, _ = LinParsJAML.read_string([(elem,)], 0)
            arr.append(elem)

        return arr, i

    @staticmethod
    def read_string(text, index):
        string = LinParsJAML.remove_quotes(text[index][0])
        number = LinParsJAML.to_number(string)
        literal = LinParsJAML.to_literal(string)

        if string != literal:
            return literal, index + 1
        elif string != number:
            return number, index + 1
        return string, index + 1

    @staticmethod
    def read_elem(text, index):
        if text[index][0] == '':
            return None, index + 1
        elif text[index][0][0] == '-':
            return LinParsJAML.read_arr(text, index)
        elif LinParsJAML.separating_colon(text[index][0]) or text[index][0][-1] == ':':
            return LinParsJAML.read_dict(text, index)
        else:
            return LinParsJAML.read_string(text, index)


if __name__ == "__main__":
    print("Запущен линейный парсер кода")

    try:
        with open("schedule.json", encoding="utf8") as json_file:
            json_format = json_file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("файл с расписанием не найден")

    python_format = LinParsJSON.read_elem(json_format, 0)[0]

    print("Результат обработки:")
    print(python_format)
