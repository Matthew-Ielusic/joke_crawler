#!/bin/sh -eu

# TODO: Move this date stamp to Python.
echo $(date) >> log_feed_crawler.log
python feed_crawler.py >> log_feed_crawler.log

echo $(date) >> log_content_crawler.log
python content_crawler.py >> log_content_crawler.log
