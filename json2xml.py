"""
Author      Jamie Ghassibi
Modified    2022-06-30
Purpose     Convert flickr photo json metadata into preservica xml metadata

Use

    Put all images in pictures/, unnested.
    Run this script from its directory. It will reference the parent directory.

    File Structure

        /base-directory
        ├───json2xml-dc
        │   └───json2xml.py  # THIS SCRIPT
        ├───json
        │   ├───data_part1
        │   │   ├───albums.json  # data_part1/ contains extra json files for album information, etc
        │   │   ├───photo_00000000.json
        │   │   └───...
        │   ├───data_part2
        │   │   ├───photo_00000000.json  # The rest of the data directories are json metadata for photos
        │   │   └───...
        │   └───...
        ├───pictures
        │   └───_d__3555_00000000_o.jpg  # The picture files don't have the same names as the pictures, but the ID is embedded
        └───xml
            └───_d__3555_00000000_o.xml  # I use the same name as the picture to name to xml file

"""

from pprint import pprint
import datetime
import json
import os
import pathlib
import subprocess
import sys

# Output progress for every N number of json files converted.
print_increment = 1000

# Run the program on N files. Set to a high number to run on all files.
run_limit = 999999

# Skip the first N files.
start_index = 32000

# The path to the albums.json file
albums_path = 'e:/flickr-downloads/test/json/data_part1/albums.json'

# Determine if the XML file be named after the jpg or the json file
BASEFILENAME = {'jpg': 0, 'json': 1}['jpg']

json2xml_fields = {
    'name': 'title',
    'description': 'description',
    'date_taken': 'date',
    'tags': 'tags',
    }

def main():

    # Create directory variables
    os.chdir('..')
    pic_dir = pathlib.Path('pictures')
    json_dir = pathlib.Path('json')

    # Check that the directory structure is setup
    if not os.path.exists(pic_dir):
        raise Exception('Directory `pictures` must exist and be populated.')
    if not os.path.exists(json_dir):
        raise Exception('Directory `json` must exist and be populated.')
    if not os.path.exists('xml'):
        os.system(f'mkdir xml')

    # Load albums.json
    albums = load_albums(albums_path)

    # Begin conversion
    print('\nBegin conversion process...', flush=True)
    file_count = start_index
    for photo_index, jpg_filename in enumerate(pic_dir.iterdir()):
        # Skip files until start index is reached.
        # This allows the user to choose to restart the process roughly where they left off.
        if photo_index < start_index:
            continue
        photo_id, json_filename = find_json(jpg_filename)
        # Skip if the json file is not found for the ID
        if json_filename is None:
            continue
        file_count += 1
        photo_json = get_json(json_filename)
        album_memberships = find_albums(photo_id, albums)
        xml_file = flickr2dc(jpg_filename, json_filename, photo_id, photo_json, album_memberships)
        if not file_count % print_increment:
            print(f'\t{str(datetime.datetime.now())[11:16]} {file_count} files done', flush=True)
        if file_count >= run_limit:
            break
    print(f'\n{file_count} files converted', flush=True)
    print('number of json files not found: ', end='', flush=True)
    os.system('wc -l json_not_found')

def find_json(jpg_filename):
    """Find the corresponding json file for a photo"""
    """If the json is not found, output the photo name to json_not_found.txt"""
    try:
        photo_id = str(jpg_filename).split('_')[-2]
        json_filename = f'photo_{photo_id}.json'
        json_filename = find(json_filename, 'json')
        if not json_filename:
            with open('json_not_found.txt', 'a') as file:
                file.write(str(jpg_filename) + '\n')
        return photo_id, json_filename
    except Exception as e:
        print('ERROR: ', jpg_filename)
        print(e)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def load_albums(albums_path):
    """Return list of all albums"""
    with open(albums_path) as file:
        return json.load(file)['albums']

def find_albums(photo_id, albums):
    album_memberships = []
    for album in albums:
        if photo_id in album['photos']:
            album_memberships.append(album['title'])
    return ','.join(album_memberships)

def get_json(json_filename):
    with open(json_filename) as file:
        return list(json.load(file).items())

def flickr2dc(jpg_filename, json_filename, photo_id, photo_json, album_memberships):
    xml_filename = make_xml_file([jpg_filename, json_filename][BASEFILENAME])
    filetered_fields = filter_fields(photo_json, json2xml_fields)
    added_fields = add_fields(filetered_fields, jpg_filename, album_memberships)
    xml_string = list2xml(added_fields)
    with open(xml_filename, 'w') as file:
        file.write(xml_string)
    return xml_filename

def filter_fields(json_data, fields):
    filtered_data = []
    for k, v in json_data:
        if k == 'tags':
            v = ','.join(tag['tag'] for tag in v)
        if k in fields:
            k = 'dc:' + fields[k]
            filtered_data.append((k, v))
    return filtered_data

def get_tags(tags):
    return [tag['tag'] for tag in tags]

def add_fields(json_data, jpg_filename, album_memberships):
    default_xml_fields = (
        ('contributer', 'Institution: Northern Essex Community College'),
        ('type', 'still image'),
        ('type', 'Photographs'),
        ('format', 'jpg'),
        ('albums', album_memberships),
        ('identifier', str(jpg_filename).split('\\')[1]),
        ('coverage', get_coverage(json_data)),
    )
    for field, value in default_xml_fields:
        json_data.append(('dc:' + field, value))
    return json_data

def make_name(title, first_tag, jpg_filename):
    if title in jpg_filename:
        return f'{title} {first_tag}'
    return title

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

def make_xml_file(base_name):
    extension = pathlib.Path(base_name).suffix
    return pathlib.Path('xml') / pathlib.Path(base_name).name.replace(extension, '.xml')

def inspect(title, data, use_pprint=True):
    print(title.upper())
    pprint(data) if use_pprint else print(data)
    print()

main()

