#!/bin/sh -eu

# TODO: Move this date stamp to Python.
TO_HERE="${BASH_SOURCE[0]}";
THIS_FILE=$(basename $TO_HERE)

TO_THIS_DIR=${TO_HERE%$THIS_FILE}

cd $TO_THIS_DIR

echo $(date) >> log_feed_crawler.log
python feed_crawler.py >> log_feed_crawler.log

echo $(date) >> log_content_crawler.log
python content_crawler.py >> log_content_crawler.log
