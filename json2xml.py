import json
import xml

jsonpath = r'sample-files/photo_4583705695.json'

json2xml_fields = {
    'name': 'title',
    'description': 'subject',
    'date_taken': 'date',
    'geo': 'latitude, longitude, accuracy',
    'tags': '????????????'
    }

def main():
    with open(jsonpath) as file:
        data = json.load(file)
    filtered_data = filter_fields(data, json2xml_fields)
    examine(filtered_data)

def filter_fields(data, fields):
    filtered_data = {}
    for k, v in data.items():
        if k == 'tags':
            v = [tag['tag'] for tag in v]
        if k in fields:
            filtered_data[k] = v
    return filtered_data

def examine(data):
    for k, v in data.items():
        print(k, v, sep=': ')


main()
