import yaml
import xml.etree.ElementTree as ET


def libConvXML(python_format):
    root = ET.Element("root")

    def make_child_tags(elem, parent_tag):
        for key, value in elem.items():
            if isinstance(value, dict):
                child_tag = ET.SubElement(parent_tag, key)
                make_child_tags(value, child_tag)
            else:
                if value is None:
                    key = key.strip()
                    ET.SubElement(parent_tag, key)
                else:
                    key = key.strip()
                    ET.SubElement(parent_tag, key).text = str(value)

    for elem in python_format:
        sub_elem = ET.SubElement(root, "element")
        make_child_tags(elem, sub_elem)

    tree = ET.ElementTree(root)
    ET.indent(tree, '   ')
    tree.write("schedule.xml", encoding='utf-8')


def libParseYAML(yaml_file_text):
    return yaml.safe_load(yaml_file_text)
