import pymongo
import feedCrawl
import crawlContent
from dbco import db
from joke import Joke
import hgp_jokes


# TODO: Fetch jokes we saw posted at least a week ago
jokes = db.jokes.find({'content': ''}).limit(100)

jokes = map(lambda joke: Joke.fromJson(joke), jokes)

crawlContent.crawlContent(jokes)

hgp_jokes.saveJokes(jokes)
