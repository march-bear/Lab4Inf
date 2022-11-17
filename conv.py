class ConvToXML:
    @staticmethod
    def write_elem(file, elem, level):
        if isinstance(elem, list):
            for i in elem:
                if isinstance(i, list) or isinstance(i, dict):
                    file.write('\t' * level + '<element>\n')
                    ConvToXML.write_elem(file, i, level + 1)
                    file.write('\t' * level + '</element>\n')
                elif i is not None:
                    file.write('\t' * level + '<element>' + str(i) + '</element>\n')
                else:
                    file.write('\t' * level + '<element/>\n')

        elif isinstance(elem, dict):
            for key, value in elem.items():
                if isinstance(value, list) or isinstance(value, dict):
                    file.write('\t' * level + f'<{key}>\n')
                    ConvToXML.write_elem(file, value, level + 1)
                    file.write('\t' * level + f'</{key}>\n')
                elif value is not None:
                    file.write('\t' * level + f'<{key}>' + str(value) + f'</{key}>\n')
                else:
                    file.write('\t' * level + f'<{key}/>\n')

    @staticmethod
    def write_format(python_format):
        xml_file = open("schedule.xml", 'w', encoding='utf8')
        xml_file.write('<?xml version="1.0"?>\n')
        xml_file.write('<root>\n')
        ConvToXML.write_elem(xml_file, python_format, 1)
        xml_file.write('</root>\n')
        xml_file.close()


class ConvToCSV:
    @staticmethod
    def write_values(python_format):
        print("EFE")
        tags = ConvToCSV.define_tags(python_format[0], '')
        values = ConvToCSV.define_values(python_format)
        csv_file = open("schedule.csv", 'w', encoding='utf8')
        print(*tags, sep=',', file=csv_file)
        for elem in values:
            print(*elem, sep=',', file=csv_file)
        csv_file.close()

    @staticmethod
    def define_values(python_format):
        values = []

        def define_other_values(format_dict):
            other_values = []
            print(format_dict)
            for _, value in format_dict.items():
                if isinstance(value, dict):
                    other_values += define_other_values(value)
                else:
                    if value is None:
                        value = ''
                    other_values.append(value)
            return other_values

        for elem in python_format:
            values.append(define_other_values(elem))
        return values

    @staticmethod
    def define_tags(format_dict, prefix):
        tags = []
        for key, value in format_dict.items():
            if isinstance(value, dict):
                tags += ConvToCSV.define_tags(value, f'{prefix}{key}/')
            else:
                tags.append(prefix + key)
        return tags

