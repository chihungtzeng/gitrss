# -*- coding: utf-8 -*-
"""
Utility functions that interacts with shell.
"""

from __future__ import print_function, unicode_literals, absolute_import
import logging
import sys
import subprocess


def run_command(cmd, cwd=None):
    """Call shell command and return the command output. The returned value
    is the stdout of the command. It has no stderr.

    Args:
    cmd -- A list of strings that make of a shell command.
    cwd -- The working directory where |cmd| is invoked.
    """
    try:
        return subprocess.check_output(cmd, cwd=cwd)
    except subprocess.CalledProcessError:
        logging.info("The command " + " ".join(cmd) + " returns non-zero code")
