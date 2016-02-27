from urllib import urlopen
from bs4 import BeautifulSoup

from pymongo import MongoClient, errors

from dateutil import parser
from datetime import datetime
import time
import pytz

from stamps import * # saving last stamps

from crawlContent import *

from joke import Joke
from hgp_jokes import saveJokes

def crawlFeed(source, feedName, feedUrl):
    """Crawl an RSS feed.

    Arguments:
    source -- Main name of the site (e.g. Reddit).
    feedName -- The title of the RSS feed (e.g. 'reddit_humor', 'reddit_jokes').
    feedUrl -- An RSS feed url to extract links from (e.g. 'http://*.rss').

    Get the jokes with their basic params: title, content, source, sourceURL, guid, pubdate
    """

    startStamp = loadLastStamp(feedName)
    latestStamp = startStamp

    epoch = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)
    html = urlopen(feedUrl).read()
    soup = BeautifulSoup(html, 'html.parser')

    foundJokes = []

    for item in soup.find_all('entry'):
        pubdate = extractPubTime(item, source)
        guid = extractGuid(item, source)
        sourceUrl = extractLink(item, source)
        title = extractTitle(item, source)

        timestamp = (pubdate - epoch).total_seconds() # Hacky way of going from Datetime object to timestamp

        if timestamp > startStamp:
            latestStamp = max(timestamp, latestStamp)

            content = ""
            aJoke = Joke(content, source, sourceUrl, guid, pubdate, title=title)
            print aJoke
            foundJokes.append(aJoke)

    print "Discovered {} jokes from {}".format(len(foundJokes), feedName)
    # crawlContent(foundJokes) # crawls for joke contents
    saveJokes(foundJokes) # save to Database

    saveLastStamp(feedName, latestStamp) # Save timestamp

def extractPubTime(item, source):
    """Create a DateTime object from a BeautifulSoup object that's probably a date.

    Arguments:
    item -- A soup object.
    """
    if source == 'reddit':
        pubdate = item.find('updated').text
        dt = parser.parse(pubdate) # String to Datetime
        return dt

    return None
    # return dt.replace(tzinfo=pytz.utc)

def extractGuid(item, source):
    """Extract a GUID from the HTML source.

    Every unique article needs a unique GUID. If two articles have the same GUID, they are
    considered to be the same.
    """
    guidItem = item.find('guid')
    if guidItem is not None:
        guid = guidItem.text
        return guid
    return ''

def extractLink(item, source):
    """Extract a canonical link from the article.

    Arguments:
    item -- A BeautifulSoup object.
    """
    if source == "reddit":
        link = item.find('link').text
        return link

    return ''


def extractTitle(item, source):
    """Extract a title from the article.

    Arguments:
    item -- A BeautifulSoup object.
    source -- A source site. Ex: 'reddit'
    """

    if source == "reddit":
        title = item.find('title').text
        return title

    return ''
