import pymongo
import feedCrawl
import crawlContent
from dbco import db
from joke import Joke
import hgp_jokes
from datetime import datetime, timedelta
import time


NUM_JOKES = 30

start_time = time.time()

now = datetime.now()
week_difference = timedelta(days=7)
week_ago = now - week_difference

# TODO: Fetch jokes we saw posted at least a week ago
jokes = db.jokes.find(
    {
        'content': {
            # Content not found
            "$in": [None, '']
        },
        'pubdate':
        {
            # Published at least a week ago
            '$lt': week_ago,
        },
        'visited': {
            # Unvisited
            '$in': [None, False]
        }
    }).limit(NUM_JOKES)

if jokes:
    # Convert joke json to Joke objects
    jokes = map(lambda joke: Joke.fromJson(joke), jokes)
    crawlContent.crawlContent(jokes)
    hgp_jokes.saveJokes(jokes)
    print jokes

print("--- %s seconds ---" % round(time.time() - start_time, 2))
