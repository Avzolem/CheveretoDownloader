# CheveretoDownloader
Python script to download albums from Chevereto


# Information
Created using Python 3.9

Initially written to support downloads of Putmega albums but should support all Chevereto based sites (untested on sites with infinite scroll)

The script creates a new folder with the title of the album and downloads all images within the album into that folder


# Installation
1. Install Python. You must select the option to add Python to PATH
![0001_add_Python_to_Path.png](https://s1.putme.ga/0001_add_Python_to_Path.png)
2. Download the latest release from https://github.com/MandoCoding/CheveretoDownloader/releases and extract
3. Run Start.bat to install all the necessary pre-requisites and start the download script


# Use
Enter Album URLs in the URLs.txt file, each URL must be on a new line

Run 'Start.bat' or the script itself 'CheveretoDownloader.py'

The script will scrape all the image links from the album and then download them into a new folder with the album name 


# Supported Sites
So far this tool has been tested and confirmed working with the following sites:

https://putme.ga/

https://pixl.is/


# Planned Future Improvements
Test with infinite scroll

Windows GUI to remove need for Python install

Cyberdrop and other site support?
