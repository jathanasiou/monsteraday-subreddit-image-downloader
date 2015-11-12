import glob
import os
import re
import sys
import praw
import requests
from bs4 import BeautifulSoup

targetSubreddit = 'monsteraday'
MIN_SCORE = 0  # the default minimum score before it is downloaded
DL_Directory = 'archive'
separator = '-------------------------------------------'
bRemoveDayNumber = True
approvedPosters = set(["StoneStrix"])

if len(sys.argv) < 2:
    # no command line options sent:
    print('No parameters, using default options.')
    print('Downloading from /r/%s, minimum score=%d' % (targetSubreddit, MIN_SCORE))
elif len(sys.argv) >= 2:
    # the minimum score was specified:
    MIN_SCORE = int(sys.argv[1])

imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')


def downloadImage(imageUrl, localFileName):
    print('Saving as "%s" ...' % (localFileName))
    response = requests.get(imageUrl)
    if response.status_code == 200:
        if not os.path.exists(DL_Directory):
            os.mkdir(DL_Directory)

        # will overwrite existing files
        with open(os.path.join(DL_Directory, localFileName), 'wb+') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)
    else:
        print('Network error or image could not be retrieved. Moving on...')


try:
    # Attempting to connect to reddit and download the subreddit front page
    # Using UUID, maybe require user's input for agent in the future
    print("Connecting to reddit...")
    r = praw.Reddit(user_agent='9137f83d-4888-4b62-b533-14b851f82d44')

    # TODO Consider allowing user to define limit of examined submissions
    print("Retrieving submissions...")
    submissions = r.get_subreddit(targetSubreddit).get_new(limit=1000)
    # Or use one of these functions:
    #                                       .get_top_from_year(limit=25)
    #                                       .get_top_from_month(limit=25)
    #                                       .get_top_from_week(limit=25)
    #                                       .get_top_from_day(limit=25)
    #                                       .get_top_from_hour(limit=25)
    #                                       .get_top_from_all(limit=25)
except:
    print('Missing file "praw.ini, should be in same folder as .exe"')

# Process all the submissions from the front page
for submission in submissions:
    print(separator)
    print('Current URL: %s' % submission.url)
    print submission.title
    print('By: /u/%s' % submission.author)
    # Check for all the cases where we will skip a submission:
    if "imgur.com/" not in submission.url:
        print('Not imgur.com submission')
        continue  # skip non-imgur submissions

    if str(submission.author) not in approvedPosters:
        # ignoring posts not made by /u/StoneStrix or other approved poster
        print('poster %s' % (submission.author))
        print('Not approved poster submission')
        continue

    if submission.score < MIN_SCORE:
        print('submission below score limit')
        continue  # skip submissions that haven't even reached 100 (thought this should be rare if we're collecting
        # the "hot" submission)

    if len(glob.glob('reddit_%s_%s_*' % (targetSubreddit, submission.id))) > 0:
        continue  # we've already downloaded files for this reddit submission

    if 'http://imgur.com/a/' in submission.url:
        # This is an album submission.
        print('Submission type: album')
        saved = False

        albumId = submission.url[len('http://imgur.com/a/'):]
        htmlSource = requests.get(submission.url).text

        soup = BeautifulSoup(htmlSource, "lxml")
        matches = soup.select('.album-view-image-link a')
        for match in matches:
            imageUrl = match['href']
            if '?' in imageUrl:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
            else:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:]
            localFileName = 'reddit_%s_%s_album_%s_imgur_%s' % (targetSubreddit, submission.id, albumId, imageFile)

            imageUrl = 'http:' + match['href']
            fileExtension = imageUrl[imageUrl.rfind('.'):]
            localFileName = submission.title + fileExtension

            if (':' in localFileName) and bRemoveDayNumber:
                localFileName = localFileName[localFileName.find(':') + 2:]

            downloadImage(imageUrl, localFileName)
            saved = True
        if not saved:
            print('No image could be retrieved.')

    elif 'http://i.imgur.com/' in submission.url:
        print('Submission type: direct image')
        # The URL is a direct link to the image.
        mo = imgurUrlPattern.search(
            submission.url)  # using regex here instead of BeautifulSoup because we are parsing a url, not html

        imgurFilename = mo.group(2)
        if '?' in imgurFilename:
            # The regex doesn't catch a "?" at the end of the filename, so we remove it here.
            imgurFilename = imgurFilename[:imgurFilename.find('?')]

        fileExtension = imgurFilename[imgurFilename.rfind('.'):]
        localFileName = submission.title + fileExtension

        if (':' in localFileName) and bRemoveDayNumber:
            localFileName = localFileName[localFileName.find(':') + 2:]

        downloadImage(submission.url, localFileName)

    elif 'http://imgur.com/' in submission.url:
        # This is an Imgur page with a single image.
        print('Submission type: imgur page')
        saved = False

        htmlSource = requests.get(submission.url).text  # download the image's page
        soup = BeautifulSoup(htmlSource, "lxml")
        matches = soup.select('a.zoom')
        for match in matches:
            imageUrl = match['href']
            if imageUrl.startswith('//'):
                # if no schema is supplied in the url, prepend 'http:' to it
                imageUrl = 'http:' + imageUrl
            imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]

            if '?' in imageUrl:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
            else:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:]

            fileExtension = imageUrl[imageUrl.rfind('.'):]
            localFileName = submission.title + fileExtension

            if (':' in localFileName) and bRemoveDayNumber:
                localFileName = localFileName[localFileName.find(':') + 2:]

            downloadImage(imageUrl, localFileName)
            saved = True
        if not saved:
            print('No image could be retrieved.')

input('Press any button to exit the script.')
