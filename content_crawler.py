import pymongo
import feedCrawl
import crawlContent
from dbco import db
from joke import Joke
import hgp_jokes
from datetime import datetime, timedelta
import time

start_time = time.time()

now = datetime.now()
week_difference = timedelta(days=7)
week_ago = now - week_difference

# TODO: Fetch jokes we saw posted at least a week ago
jokes = db.jokes.find(
    {
        'content': '',
        'pubdate':
        {
            '$lt': week_ago,
        }
    }).limit(20)

if jokes:
    jokes = map(lambda joke: Joke.fromJson(joke), jokes)
    crawlContent.crawlContent(jokes)
    hgp_jokes.saveJokes(jokes)
    print jokes

print("--- %s seconds ---" % round(time.time() - start_time, 2))
