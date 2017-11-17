#!/bin/bash
set -x
readonly top=$(readlink -e $(dirname $0))
repo=/home/clark/openSource/chromium.git/src
repo=/home/clark/work/experiments
export PYTHONPATH=${top}:${top}/gitlog2rss
python -m gitlog2rss \
--repo-path ${repo} --output-file /mnt/ramdisk/rss.xml
