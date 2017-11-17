#!/bin/bash
set -x
readonly top=$(readlink -e $(dirname $0))
repo=~/openSource/chromium.git/src
export PYTHONPATH=${top}:${top}/gitrss
python -m gitrss --repo ${repo} --output-file /mnt/ramdisk/rss.xml
