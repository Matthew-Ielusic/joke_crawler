#!/bin/sh -eu

# TODO: Move this date stamp to Python.
TO_HERE="${BASH_SOURCE[0]}";
THIS_FILE=$(basename $TO_HERE)

TO_THIS_DIR=${TO_HERE%$THIS_FILE}

echo $TO_THIS_DIR;

cd $TO_THIS_DIR

echo $(date) >> crawler_runs.log
python crawler.py >> crawler_runs.log

