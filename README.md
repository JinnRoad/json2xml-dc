
# Download and transform Flickr files into Preservica-accepted files

## Summary

This directory contains two scripts:
```
	download_flickr_files.py
	json2xml.py
```

```
download_flickr_files.py
	This script downloads and unzips folders from flickr into
		files/json	(metadata files)
			json_part1/
			json_part2/
			...
		files/media	(photos and videos)
			media_1/
			media_2/
			...

	The first json dir contains `albums.json`, which describes which album each photo belongs to.

json2xml.py
	This script converts the json data files to xml for importing into Preservica.
	Some additional data is put is. For example:
	-	Searching albums.json to determine which album each photo belongs to
	-	Determining the location where the photo was taken.
```

## Downloading from Flickr

1.	Request flickr to prepare files for download. Flickr may take a few DAYS to finish. M. Hearn can show you how this is done.

2.	On the Settings page, scroll down until you see "Your Flickr Data". There will be two sections of files:
	1.	Account Data (which is the metadata)
	2.	Photos and Videos

3.	Make a list of all the links for these files:
	1.	Copy the first link in Account Data, which will look something like this:

		https://s3.amazonaws.com/flickr-metadump-us-east-1/..._part1.zip

		Notice the last part of that file is "part1".
		Use some tool (vim, bash, etc) to quickly make a list of files like:

		https://s3.amazonaws.com/flickr-metadump-us-east-1/..._part1.zip
		https://s3.amazonaws.com/flickr-metadump-us-east-1/..._part2.zip
		.
		.
		.
		https://s3.amazonaws.com/flickr-metadump-us-east-1/..._part10.zip

	2.	Repeat the same process for the links in the Photos and Videos section:

		https://downloads.flickr.com/d/data_..._1.zip
		https://downloads.flickr.com/d/data_..._2.zip
		.
		.
		.
		https://downloads.flickr.com/d/data_..._150.zip
