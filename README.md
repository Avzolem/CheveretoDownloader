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
Once all the installation steps are complete you can either double click on 'Start.bat' or the script itself 'CheveretoDownloader.py'

Enter a URL when required and press enter

The script will then scrape all the image links from the album and download them into a new folder with the album name 


# Planned Future Improvements
Multi-threaded Downloads

Error retry

Bulk Downloader for multiple album URLs

Cyberdrop and other site support?
