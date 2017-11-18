#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run unittest tests in the repository."""
from __future__ import print_function
import glob
import os
import sys
import subprocess
from py_check import get_commit_files


def get_repo_path():
    """
    Return the full path of the repository.
    """
    script_path = os.path.abspath(os.path.join(__file__, ".."))
    # Return the path that contains a .git directory
    cur = script_path
    while True:
        repo_dir = os.path.join(cur, ".git")
        if os.path.isdir(repo_dir):
            return cur
        else:
            cur = os.path.normpath(os.path.join(cur, ".."))


def get_possible_src_paths():
    """
    Given a repository named foo, source files may be in foo/ or foo/foo/.
    This function returns all these possibilities.
    """
    repo_path = get_repo_path()
    repo_name = os.path.split(repo_path)[1]
    return [repo_path, os.path.join(repo_path, repo_name)]


def get_unittests():
    """
    Return:
    A list of unittests (*.py files) in full path
    """
    src_paths = get_possible_src_paths()
    test_paths = [os.path.join(item, "test") for item in src_paths]

    result = []
    for test_path in test_paths:
        result += glob.glob(test_path + os.sep + "unittest_*.py")
    return result


def main():
    """Executable entry"""
    os.environ["PYTHONPATH"] = ":".join(get_possible_src_paths())
    print(u"PYTHONPATH={}".format(os.environ["PYTHONPATH"]))
    commit_files = get_commit_files()

    for _ut in get_unittests():
        _, base_name = os.path.split(_ut)
        src = base_name.replace("unittest_", "")
        cmd = ["python", _ut]
        print(" ".join(cmd))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            print(output)
            output_lines = output.splitlines()
            if "OK" not in output_lines[-1]:
                return 1
        except subprocess.CalledProcessError as e:
            print("Trouble: " + _ut)
            print("output:")
            print(e.output)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
