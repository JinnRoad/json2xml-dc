"""
Dependencies
    git-bash

Instructions

    Create file directory like so

        # Output Directory
        [some path]/files
        [some path]/files/json
        [some path]/files/media

    Choose the stop time. This download process can be lengthy, so choose a time before you leave for work.

    Create a file called `flickr_file_url_list` of all the URLs you wish to download.
    This can be created easily by copy-pasting the filenames from flickr, then reformatting into a textfile using vim or similar.
    After this script successfully downloads a zip directory, it will remove the filename from `flickr_file_url_list`.
    This way, the next time this script is run, it will left off where it started.

"""

import pathlib
import datetime
import os

stoptime = '2022-08-31 12:30' # Choose a time before you leave work, so this process can stop and be continued tomorrow.

# Give the ABSOLUTE PATHS to the urls file and the output directory
# It's a good idea to make a backup of this url file, as this script will delete lines as it finishes them
urls_file = pathlib.Path(r'E:\flickr-downloads\json2xml-dc\urls.txt')
#output_directory = pathlib.Path(r'E:\flickr-downloads\files')
output_directory = pathlib.Path(r'E:\flickr-downloads\files-download-test')

def main():

    # Curl is used in download() to download files.
    # Curl cannot save to absolute paths for some reason, so we must cd to the output directory
    os.chdir(output_directory)

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
        unzip(download(url))
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
            file.write(url)

def time_to_stop(stoptime):
    # Check if current time > stop time
    return datetime.datetime.now() > datetime.datetime.strptime(stoptime, '%Y-%m-%d %H:%M')

main()
