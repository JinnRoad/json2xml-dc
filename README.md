This directory contains two scripts:
	download_flickr_files.py
	json2xml.py

download_flickr_files.py
	This script downloads zip files from flickr.
	These zip files contain photo files as well as data directories with json metadata for these photos.
	The first data directory contains an albums.json file that describes what albums each photo belongs to.

json2xml.py
	This script converts the json data files to xml for importing into Preservica.
	Some additional data is put is. For example:
	-	Searching albums.json to determine which album each photo belongs to
	-	Determining the location where the photo was taken.

Issues
-	Loading jpg files plus their xml metadata does not seem to work for Preservica.
-	From my research, what may need to be done is to completely change the script to output a single csv file containing all metadata.
-	I recommend testing this with one or two photos first, with a metadata file that is just contains information on these two files.
