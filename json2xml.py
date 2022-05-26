# Changes
#   Use list structure instead of dictionary

import json
from xml.etree.ElementTree import Element, tostring
from dicttoxml import dicttoxml

jsonpath = r'sample-files/photo_4583705695.json'

json2xml_fields = {
    'name': 'title',
    'description': 'description',
    'date_taken': 'date',
    'tags': 'tags', # se filtered_data
    }

default_fields = {
    'type': 'Photographs',
}

def main():
    with open(jsonpath) as file:
        json_data = json.load(file)
    list_data = json2list(json_data, json2xml_fields)
    examine(list_data)
    #xml_data = dict_to_xml_CHANGE('TEST', list_data) # change to list2xml
    print()
    #print(tostring(xml_data))
    #print(dicttoxml(filtered_data))

def json2list(data, fields):
    filtered_data = []
    for k, v in data.items():
        if k == 'tags':
            v = ','.join(tag['tag'] for tag in v)
        if k in fields:
            k = 'dc:' + fields[k]
            filtered_data.append((k, v))
    return filtered_data

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

def examine(data):
    for k, v in data:
        print(k, v, sep='  ')

main()
