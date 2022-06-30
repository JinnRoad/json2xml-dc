"""
Instructions

    Choose the output directory.
    Choose the stop time. This download process can be lengthy, so choose a time before you leave for work.
    Choose a filename_prefix. The default, 'data-download-' should be fine.

    Create a file called `flickr_file_url_list` of all the URLs you wish to download.
    This can be created easily by copy-pasting the filenames from flickr, then reformatting into a textfile using vim or similar.
    After this script successfully downloads a zip directory, it will remove the filename from `flickr_file_url_list`.
    This way, the next time this script is run, it will left off where it started.

"""

import datetime
import os

output_directory = 'D:/flickr-downloads'
stoptime = '2022-05-17 13:46' # Half an hour before you leave work, so this process can stop and be continued tomorrow.
filename_prefix = 'data-download-'
urls_file = 'flickr_file_url_list.txt'

def main():
    pwd = os.getcwd()
    with open(urls_file) as file:
        urls = list(file)
    while urls:
        if time_to_stop(stoptime):
            print('-'*40)
            print('\nscript ended early for the end of the work day. Please continue tomorrow.')
            return
        url = urls.pop(0)
        get_file(url)
        update_list(pwd, urls_file, urls)

def get_file(url):
    os.chdir(output_directory) # Curl cannot save to absolute paths, so we must change directory
    url = url.strip()
    filename = filename_prefix + url.split('_')[-1]
    print(f'downloading {filename}', flush=True)
    os.system(f'curl {url} -o {filename}')
    print('\n', flush=True)

def update_list(pwd, urls_file, urls):
    os.chdir(pwd)
    with open(urls_file, 'w') as file:
        for url in urls:
            file.write(url)

def time_to_stop(stoptime):
    return datetime.datetime.now() > datetime.datetime.strptime(stoptime, '%Y-%m-%d %H:%M')

main()
