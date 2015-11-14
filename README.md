#Monster-a-day Image Downloader

Based on asweigart/imgur-hosted-reddit-posted-downloader tool.
This fork checks the **/r/monsteraday subreddit** and attempts to download all the images linked from there by the sub's creator, **/u/StoneStrix**. Given no parameters, the script will create a /archive directory in the folder it is run from and store/overwrite all downloaded images there. Saved files will be automatically named according to their submission title in Reddit.  
Hopefully soon there will be options to affect format/quality too.

##Requirements and info:
No matter how it's run, the script will create a folder called **"archive"** and download all eligible images there. Currently this means any imgur-hosted link which was posted by /u/StoneStrix. Furthermore, the submission titles(which are used as filanames) will be renamed so that the 'Day x:' part is removed and entries are saved alphabetically.
###Linux
When running via **Linux** you need to have **Python2** installed as well as the following Python libraries, which can be retrieved either via **pip** or your distro's **package manager**.  

* praw
* requests
* beautifulsoup4
* lxml

Then simply download the .py script and follow the command-line instructions below.

###Windows
For ease of use it is recommended that you download the **/dist/** folder's files in a location of your choice and run the .exe from there. Just make sure it's in the *same location as the praw.ini* file as well.  
Intermediate users might also want to download **Python 2** and install it normally, following the various instructions online as well as getting the libraries mentioned in the Linux section above. Afterwards one could either run it via command-promt(read below) or simply double click the .py file.

##Command-line usage:

###No parameters

`$ python monsteraday-image-downloader.py`

###Defining minimum score to download (default 0)

`$ python monsteraday-image-downloader.py 50`

If there are multiple versions of python installed, it may be necessary to use `$ ptyhon2` instead of `$ python` in systems where more than one version of python is installed and python2 is not the default python environment.
