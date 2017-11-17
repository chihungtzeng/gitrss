#!/usr/bin/env python
"""Check consistent coding style."""
from __future__ import print_function
import os
import sys
import subprocess
import tempfile
import filecmp


def get_commit_files():
    """Get the committed files and return them as a list."""
    cmd = ["git", "diff", "--cached", "--name-only"]
    commit_files = subprocess.check_output(cmd)
    return commit_files.splitlines()


def _check_py_style(filename):
    """Check python coding style using pep8"""
    ret = subprocess.call(["pep8", filename])
    if ret != 0:
        print(filename + " not comply to pep8.")
        return False

    ret = subprocess.call(["pylint", "-E", filename])
    if ret != 0:
        print(filename + " not comply to pylint -E.")
        return False

    print("OK. " + filename + " passes pep8 and pylint check.")
    return True


def _is_style_consistent(filename):
    """Return True if coding style is met and False otherwise"""
    _path, ext = os.path.splitext(filename)
    if ext == ".py":
        if os.path.isfile(filename):
            return _check_py_style(filename)
        else:
            # File is deleted, so return True unconditionally.
            return True
    else:
        print("No style checker for " + filename)
        return True


def main():
    """Executable entry"""
    commit_files = get_commit_files()
    fail_count = 0
    for filename in commit_files:
        if not _is_style_consistent(filename):
            fail_count += 1
    return fail_count


if __name__ == "__main__":
    sys.exit(main())
