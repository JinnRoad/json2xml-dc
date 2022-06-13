# TODO Add comments
# TODO Convert lists to XML

import json
from pprint import pprint
import pathlib

json2xml_fields = {
    'name': 'title',
    'description': 'description',
    'date_taken': 'date',
    'tags': 'tags',
    }

def flickr2dc(json_path):
    with open(json_path) as file:
        list_data = list(json.load(file).items())
    inspect('json', list_data)
    filtered_json = filter_fields(list_data, json2xml_fields)
    inspect('filtered', filtered_json)
    added_json = add_fields(filtered_json, json_path)
    inspect('fields added', added_json)
    xml_string = list2xml(added_json) # change to list2xml
    inspect('xml string', xml_string, use_pprint=False)
    xml_name = make_xml_file(json_path)
    with open(xml_name, 'w') as file:
        file.write(xml_string)

def filter_fields(json_data, fields):
    filtered_data = []
    for k, v in json_data:
        if k == 'tags':
            v = ','.join(tag['tag'] for tag in v)
        if k in fields:
            k = 'dc:' + fields[k]
            filtered_data.append((k, v))
    return filtered_data

def add_fields(json_data, json_path):
    # Use list as look up and keys{}, vals{} are unnecessary.
    default_xml_fields = {
        'subject': '',
        'type': 'Photographs',
        'identifier': (get_id, json_path),
        'coverage': (get_coverage, json_data),
    }
    for k, v in default_xml_fields.items():
        # Values are usually strings, but if a function is at index
        # 0, then call the function using the parameters in the rest
        # of the value.
        try:
            if callable(v[0]):
                f = v[0]
                args = v[1:]
                v = f(*args)
        except IndexError:
            pass
        json_data.append(('dc:' + k, v))
    return json_data

def get_id(json_path):
    return pathlib.Path(json_path).stem

def get_coverage(json_data):
    for field, value in json_data:
        if 'tags' in field:
            if 'lawrence' in value.lower():
                return 'Lawrence'
            if 'haverhill' in value.lower():
                return 'Haverhill'
            return ''

def list2xml(list_data):
    xml_header = '<oai_dc:dc xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/oai_dc.xsd">'
    xml_footer = '</oai_dc:dc>'
    xml_list = []
    xml_list.append(xml_header)
    for field, value in list_data:
        xml_list.append(f'    <{field}>{value}</{field}>')
    xml_list.append(xml_footer)
    return '\n'.join(xml_list)

def make_xml_file(json_path):
    return pathlib.Path(json_path).with_suffix('.xml')

def inspect(title, data, use_pprint=True):
    print(title)
    pprint(data) if use_pprint else print(data)
    print()

json_path = r'sample-files/photo_4583705695.json'
flickr2dc(json_path)
