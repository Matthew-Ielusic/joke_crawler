#!/bin/sh -eu

# TODO: Move this date stamp to Python.
echo $(date) >> crawler_runs.log
python crawler.py >> crawler_runs.log
