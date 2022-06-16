# TODO Add comments
# TODO look for the album information JSON on the external storage. use <dc:album></dc:album>.
# TODO allow to run on entire directory, probably using pathlib
# TODO ? I have tags like BillZanini. Do you want these converted to Bill Zanini?

from pprint import pprint
import json
import pathlib
import sys
import os

limit = 50

def main():
    if not os.path.exists('xml'):
        os.system(f'mkdir xml')
    directory = pathlib.Path('json')
    glob_str = 'photo_*.json'
    file_count = 0
    for json_file in directory.glob(glob_str):
        xml_file = flickr2dc(json_file)
        file_count += 1
        if file_count > limit:
            break
    print(f'done: {file_count} files', flush=True)

json2xml_fields = {
    'name': 'title',
    'description': 'description',
    'date_taken': 'date',
    'tags': 'tags',
    }

def flickr2dc(json_file):
    with open(json_file) as file:
        list_data = list(json.load(file).items())
    #inspect('json', list_data)
    filtered_json = filter_fields(list_data, json2xml_fields)
    #inspect('filtered', filtered_json)
    added_json = add_fields(filtered_json, json_file)
    #inspect('fields added', added_json)
    xml_string = list2xml(added_json)
    #inspect('xml string', xml_string, use_pprint=False)
    xml_file = make_xml_file(json_file)
    with open(xml_file, 'w') as file:
        file.write(xml_string)
    return xml_file

def filter_fields(json_data, fields):
    filtered_data = []
    for k, v in json_data:
        if k == 'tags':
            v = ','.join(tag['tag'] for tag in v)
        if k in fields:
            k = 'dc:' + fields[k]
            filtered_data.append((k, v))
    return filtered_data

def add_fields(json_data, json_file):
    # Use list as look up and keys{}, vals{} are unnecessary.
    default_xml_fields = (
        ('contributer', 'Institution: Northern Essex Community College'),
        ('type', 'still image'),
        ('type', 'Photographs'),
        ('format', 'jpg'),
        ('identifier', (get_id, json_file)),
        ('coverage', (get_coverage, json_data)),
    )
    for field, value in default_xml_fields:
        # Values are usually strings, but if a function is at index
        # 0, then call the function using the parameters in the rest
        # of the value.
        try:
            if callable(value[0]):
                function = value[0]
                args = value[1:]
                value = function(*args)
        except IndexError:
            pass
        if value:
            json_data.append(('dc:' + field, value))
    return json_data

def get_id(json_file):
    return pathlib.Path(json_file).stem + '.jpg'

def get_coverage(json_data):
    coverage_base = 'Massachusetts -- Essex (count) -- '
    for field, value in json_data:
        if 'tags' in field:
            if 'haverhill' in value.lower():
                return coverage_base + 'Haverhill'
            if 'lawrence' in value.lower():
                return coverage_base + 'Lawrence'
            return ''

def list2xml(list_data):
    indent1 = 8 * ' '
    indent2 = 10 * ' '
    xml_header = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'{indent1}<'
        'oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ '
        'http://www.openarchives.org/OAI/2.0/oai_dc.xsd"'
        '>'
        )
    xml_footer = f'{indent1}</oai_dc:dc>'
    xml_list = []
    xml_list.append(xml_header)
    for field, value in list_data:
        xml_list.append(f'{indent2}<{field}>{value}</{field}>')
    xml_list.append(xml_footer)
    return '\n'.join(xml_list)

def make_xml_file(json_file):
    return pathlib.Path('xml') / pathlib.Path(json_file).name.replace('.json', '.xml')

def inspect(title, data, use_pprint=True):
    print(title.upper())
    pprint(data) if use_pprint else print(data)
    print()

main()
