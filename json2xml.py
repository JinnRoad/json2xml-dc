# TODO Add comments
# TODO Convert lists to XML

import json
from pprint import pprint
from xml.etree.ElementTree import Element, tostring
from dicttoxml import dicttoxml

json_path = r'sample-files/photo_4583705695.json'

def main():
    with open(json_path) as file:
        json_data = list(json.load(file).items())
    data = filter_fields(json_data, json2xml_fields)
    pprint(data)
    data = add_fields(data, json_path)
    pprint(data)
    #picture_xml = dict2xml_CHANGE('TEST', data) # change to list2xml
    print()
    #print(tostring(picture_xml))
    #print(dicttoxml(filtered_data))

json2xml_fields = {
    'name': 'title',
    'description': 'description',
    'date_taken': 'date',
    'tags': 'tags',
    }

def filter_fields(data, fields):
    filtered_data = []
    for k, v in data:
        if k == 'tags':
            v = ','.join(tag['tag'] for tag in v)
        if k in fields:
            k = 'dc:' + fields[k]
            filtered_data.append((k, v))
    return filtered_data

def add_fields(data, json_path):
    # Use list as look up and keys{}, vals{} are unnecessary.
    default_xml_fields = {
        'subject': '',
        'type': 'Photographs',
        'identifier': (get_filename, json_path),
    }
    for k, v in default_xml_fields.items():
        # Values are usually strings, but if a function is at index
        # 0, then call the function using the parameters in the rest
        # of the value.
        try isinstance(v, str) or callable(v[0]):
            pass
        except TypeError:
            raise Exception('Value in default field is not string or tuple beginning with function', k)
        if callable(v)[0]:
            v = v(*v[1:])
        data.append((k, v))
    # TODO Add fields to input data
    # TODO Add functions as needed
    return data

def get_filename():
    pass

def list2xml(tag, d):  # TODO read through code carefully
    # From [insert website]
    raise NotImplemented
    elem = Element(tag)
    for key, val in d.items():
        # create an Element
        # class object
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

main()
