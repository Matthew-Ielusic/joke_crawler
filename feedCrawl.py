from urllib import urlopen
from bs4 import BeautifulSoup

from pymongo import MongoClient, errors

from dateutil import parser
from datetime import datetime
import time
import pytz

from stamps import * # saving last stamps

from article import *
from crawlContent import *

from joke import Joke

def crawlFeed(source, feedName, feedUrl):
    """Crawl an RSS feed.

    Arguments:
    source -- Main name of the site (e.g. Reddit).
    feedName -- The title of the RSS feed (e.g. 'reddit_humor', 'reddit_jokes').
    feedUrl -- An RSS feed url to extract links from (e.g. 'http://*.rss').

    Get the jokes with their basic params: title, content, source, sourceURL, guid, pubdate
    """

    startStamp = loadLastStamp(feedName)
    epoch = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

    html = urlopen(feedUrl).read()

    soup = BeautifulSoup(html, 'html.parser')
    latestStamp = startStamp

    foundJokes = []

    for item in soup.find_all('item'):
        pubdate = extractPubTime(item)
        guid = extractGuid(item, source)
        sourceUrl = extractLink(item)

        timestamp = (pubdate - epoch).total_seconds() # Hacky way of going from Datetime object to timestamp

        if timestamp > startStamp:
            latestStamp = max(timestamp, latestStamp)

            content = ""
            aJoke = Joke(content, source, sourceUrl, guid, pubdate)
            print aJoke
            foundJokes.append(aJoke)

    # newArticles = crawlContent(newArticles) # crawls for content, img and possible keywords (?)
    # saveNewArticles(newArticles) # save to Database
    # print feedName, " => +"+str(len(newArticles))
    # for article in newArticles:
    #     print article

    saveLastStamp(feedName, latestStamp) # save to not reload articles

def extractPubTime(item):
    """Create a DateTime object from a BeautifulSoup object that's probably a date.

    Arguments:
    item -- A soup object.
    """
    dt = parser.parse(item.pubdate.text) # String to Datetime
    return dt
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

def extractLink(item):
    """Extract a canonical link from the article.

    Arguments:
    item -- A BeautifulSoup object.
    """
    t1 = item.find('feedburner:origlink')
    t2 = item.find('link')
    if t1 is not None:
        return t1.text
    elif t2 is not None:
        return t2.text
    return ''
