@echo TITLE: Chevereto Downloader.
                                            
@echo Joint operation by some lovely people on SE initially written for Putme.ga but should support all Chevereto based sites (untested on sites with infinite scroll) 

@echo It will now try to install required modules. 

pause 

python -m pip install --upgrade pip

python -m pip install requests beautifulsoup4

@echo modules installed

python "CheveretoDownloader.py"



