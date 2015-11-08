Monster-a-day Image Downloader
=====================================

Based on asweigart/imgur-hosted-reddit-posted-downloader tool.
This fork checks the /r/monsteraday sub and attempts to download all the images linked from there. Given no parameters, the script will create a /archive directory in the folder it is run from and store/overwrite all downloaded images there. Saved files will be automatically named according to their submission title in Reddit.  
Hopefully soon there will be options to affect format/quality too.

Command-line usage:
-----

###No parameters

`python monsteraday-image-downloader.py`

###Defining minimum score to download (default 0)

`python monsteraday-image-downloader.py 50`