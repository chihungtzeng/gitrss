"""Utility functions for unit tests
"""
from __future__ import print_function
from ut_setting import OVERWRITE_EXPECTED
import os


def read_file_contents(full_path):
    """Return file contents. If the specified file does not exist, then
    return an empty string.
    """
    if not os.path.isfile(full_path):
        print("File not exist: " + full_path)
        return ""
    with file(full_path) as _fp:
        contents = _fp.read()
    return contents


def write_file_if_necessary(full_path, contents):
    """Write contents to full_path if OVERWRITE_EXPECTED is true. This
    function is used to reset test expectations.
    """
    if not OVERWRITE_EXPECTED:
        return
    if os.path.isfile(full_path):
        print("WARNING: Write to an existent file " + full_path)

    with file(full_path, "w") as _fp:
        _fp.write(contents)


def is_contents_equal(alex, bob):
    """Compare if two strings, or lists of strings, are equal. The
    comparison does not take heading and trailing spaces, "\n", and tabs
    into consideration.
    """
    if isinstance(alex, basestring):
        alex = alex.splitlines()
    if isinstance(bob, basestring):
        bob = bob.splitlines()
    if len(alex) != len(bob):
        return False
    for i in range(len(alex)):
        if alex[i].strip() != bob[i].strip():
            return False
    return True
