"""

Author: Jamie Ghassibi
Date:   2022-08-31

Dependencies
    git-bash

Instructions

    1.  Enter the filepath to the urls file and put it below in the urls_file variable.

    2.  Choose an output directory and put it below in the output_directory variable.
        If the directory doesn't exist already, it will be created.
        For example, if output directory is:
            /e/flickr-downloads/

    3.  Choose the stop time. This download process can be lengthy, so choose a time before you leave for work.

"""

import pathlib
import datetime
import os


# USER VARIABLES

# Choose a time before you leave work, so this process can stop and be continued tomorrow.
stoptime = '2022-09-01 12:30'

# Give the ABSOLUTE PATHS to the urls file and the output directory
# It's a good idea to make a backup of this url file, as this script will delete lines as it finishes them
urls_file = pathlib.Path(r'E:\flickr-downloads\json2xml-dc\urls.txt')
output_directory = pathlib.Path(r'E:\flickr-downloads\files')


def main():

    # Ensure the output directories exist. If they exist, these commands do nothing.
    # Curl is used in download() to download files.
    # Curl cannot save to absolute paths for some reason, so we must cd to the output directory
    os.system(f'mkdir {output_directory}')
    os.chdir(output_directory)
    os.system('mkdir json')
    os.system('mkdir media')
    print()

    # Get the list of URLs
    with open(urls_file) as file:
        urls = [line.strip() for line in file if line.strip()]

    while urls:

        # If the work day is almost over, stop running
        if time_to_stop(stoptime):
            print('-'*40)
            print('\nscript ended early for the end of the work day.\nplease continue tomorrow.')
            break

        # Remove URL from list. This way when the list is rewritten to urls.txt
        #   the list will be updated, so that the next time this script
        #   is run, it will pick up where it left off.
        url = urls.pop(0)

        # Download the flickr zip files, unzip them, then update the URL list
        filepath = download(url)
        unzip(filepath)
        update_list(urls_file, urls)
    print('\a')  # Bell on completion. (vim: set novisualbell)

def download(url):
    # Make the output filename
    # If 'metadump' is in the URL name, use 'json', otherwise use 'media'
    prefix = 'json' if 'metadump' in url else 'media'
    suffix = url.split('_')[-1]
    filename = pathlib.Path(prefix + '_' + suffix)

    # Change to the json or media directory, depending on the above prefix decision
    os.chdir(prefix)
    filepath = pathlib.Path(os.getcwd() / filename)
    print(f'download {filepath}', flush=True)
    os.system(f'curl {url} -o {filename}')
    print('\n', flush=True)
    os.chdir('..') # Return to parent directory
    return filepath

def unzip(filepath):
    # Make unzipped directory name: 'file.zip' -> 'file/'
    unzipped = pathlib.Path(str(filepath)[:-4])
    # Unzip file into file/
    os.system(f'7z x {filepath} -o{unzipped}')
    # If successful, delete file.zip
    if unzipped.exists():
        os.system(f'del {filepath}')

def update_list(urls_file, urls):
    # Write the updated list of URLs to the url file
    # This new list has the just-downloaded link removed
    # This allows the next run of the program to begin where it left off
    with open(urls_file, 'w') as file:
        for url in urls:
            file.write(url + '\n')

def time_to_stop(stoptime):
    # Check if current time > stop time
    return datetime.datetime.now() > datetime.datetime.strptime(stoptime, '%Y-%m-%d %H:%M')

main()
