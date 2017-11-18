# -*- coding: utf-8 -*-
"""
Helper functions for dealing with utf8.
"""
import logging


def to_utf8(string):
    """
    Return a string that can be treated as a utf-8 string.
    """
    if isinstance(string, unicode):
        return string
    else:
        try:
            return string.decode("utf-8")
        except UnicodeDecodeError:
            logging.info("Cannot decode:")
            logging.info(string)
            logging.info(type(string))
