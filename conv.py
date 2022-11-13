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


if __name__ == "__main__":
    pass
