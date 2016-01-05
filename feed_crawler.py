from feedCrawl import *
import time

start_time = time.time()

sources = ['reddit']
feeds = {}

feeds['reddit'] = []
feeds['reddit'].append({'name': 'reddit_jokes', 'url': 'https://www.reddit.com/r/jokes/.xml'})
feeds['reddit'].append({'name': 'reddit_humor', 'url': 'https://www.reddit.com/r/humor/.xml'})
feeds['reddit'].append({'name': 'reddit_funny', 'url': 'https://www.reddit.com/r/funny/.xml'})

for source in sources:
    for feed in feeds[source]:
        crawlFeed(source, feed['name'], feed['url'])
        time.sleep(2)

print("--- %s seconds ---" % round(time.time() - start_time, 2))
