#!/usr/bin/env python
"""
Write RSS file.
"""
from __future__ import unicode_literals, absolute_import
import argparse
import io
import os
import sys
from . import GitRepo


def gen_rss(repo_path, output_file):
    """
    Args:
    repo_path -- A git repository path.
    output_file -- The rss file that is written to.
    """
    git_repo = GitRepo(os.path.normpath(repo_path))
    rss_contents = git_repo.to_rss()

    if os.path.isdir(output_file):
        output_file = os.path.join(output_file, "rss.xml")

    with io.open(output_file, "w", encoding="utf-8") as _fp:
        _fp.write(rss_contents)


def main():
    """
    Program Entry.
    """
    parser = argparse.ArgumentParser(
        description="Create RSS feed for a git repository")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--output-file", default="rss.xml")
    args = parser.parse_args()
    gen_rss(args.repo, args.output_file)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
