import urllib, urllib2
from dateutil.parser import *
from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
import time
from joke import Joke
import re
import praw
from joke import Joke

AGENT_NAME = "HGP"
source_reddit = "reddit"


def crawlContent(jokes):
    """Download and crawl the URLs stored in several jokes."""

    redditAgent = praw.Reddit(user_agent=AGENT_NAME)
    for joke in jokes:
        if isinstance(joke, Joke) and joke.source == source_reddit:
            handleRedditJoke(joke, redditAgent)
    return jokes

def extractRedditSubmissionId(sourceURL):
    '''Extracts reddit submission ID from url'''

    pattern = r'.*reddit.com/r/.*/comments\/'
    leftovers = re.sub(pattern, '', sourceURL)
    leftovers_broken = leftovers.split('/')
    submissionId = leftovers_broken[0]
    return submissionId

def handleRedditJoke(joke, redditAgent):
    if isinstance(joke, Joke) and redditAgent:
        submissionId = extractRedditSubmissionId(joke.sourceURL)
        submission = redditAgent.get_submission(submission_id=submissionId)

        joke.content = submission.selftext
        joke.title = submission.title

        joke.upvotes = submission.ups
        total_votes = int(round(joke.upvotes / submission.upvote_ratio))
        joke.downvotes = total_votes - joke.upvotes

        if submission.author:
            joke.author = str(submission.author.name)

    else:
        raise ValueError
