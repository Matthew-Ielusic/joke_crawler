import pymongo
import feedCrawl
import crawlContent
from dbco import db
from joke import Joke


jokes = db.jokes.find().limit(1)

jokes = map(lambda joke: Joke.fromJson(joke), jokes)

crawlContent.crawlContent(jokes)
