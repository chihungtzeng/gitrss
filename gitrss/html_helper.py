"""
Helper functions for generating html contents.
"""
from __future__ import absolute_import, unicode_literals
import io
import logging
import os
import pprint
import sys
from jinja2 import Template
from utf8_utils import to_utf8

HTML_ESCAPE_MAP = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "\'": "&#39;",
}


def _get_data_path():
    """
    Return the full path of data/
    """
    cur_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cur_path, "data")


def _get_template_contents():
    """
    Return the contents of rss template file.
    """
    data_path = _get_data_path()
    template = os.path.join(data_path, "rss_template.xml")
    logging.info("Read RSS template from {}".format(template))
    with io.open(template, encoding="utf-8") as _fp:
        contents = _fp.read()
    return contents


def escape_html_char(text):
    """
    Replace the chars such as < with &lt and > with &gt because these chars
    are part of the html syntax.

    Args:
    text -- A string.
    """
    res = []
    text = to_utf8(text)
    for char in text:
        res.append(HTML_ESCAPE_MAP.get(char, char))
    return u"".join(res)


def gen_rss_contents(channel, rss_entries):
    """
    Generate rss file contents.
    """
    template = Template(_get_template_contents())
    renderer = getattr(template, "render")
    return renderer(channel=channel, rss_entries=rss_entries)


def open_tag(tag, attrs=None):
    """Returns a html open tag.

    Args:
    tag: A html tag
    attrs: tag attributes. Its type is dict and all its elements are str.
    """
    ret = "<" + tag
    if attrs and isinstance(attrs, dict):
        for item in sorted(attrs):
            ret += " " + item + "=\"" + attrs[item] + "\""
    return ret + ">"


def close_tag(tag):
    """Returns a close tag"""
    if tag in ["br"]:
        return ""
    else:
        return "</" + tag + ">"


def tag_block(tag, text, attrs=None):
    """Wrap text within the tag block.

    Args:
    tag: A html tag
    text: The text inside the tag block
    attrs: The attributes of the html tag
    """
    if isinstance(text, list):
        text = "".join(text)
    text = to_utf8(text)
    ret = [open_tag(tag, attrs), text, close_tag(tag)]
    return "".join(ret)


def td_block(column, td_attrs=None):
    """Wrap text within the td block"""
    return tag_block("td", column, td_attrs)


def tr_block(columns, tr_attrs=None, td_attrs=None):
    """Wrap text within the tr block, where tr is a row of an html table.
    Args:
    columns: the columns of the table row. Its type is list, whose elements
             are all str.
    tr_attrs: The attributes of tr
    td_attrs: The attributes of td, the column element.
    """
    ret = [open_tag("tr", tr_attrs)]
    for column in columns:
        ret.append(td_block(column, td_attrs))
    ret.append(close_tag("tr"))
    return "".join(ret)


def table_block(rows, table_attrs=None, tr_attrs=None, td_attrs=None):
    """Generate html table.
    Args:
    rows: Table rows, its type is a list of lists.
    table_attrs: The attributes of the table.
    tr_attrs: The attributes of rows.
    td_attrs: The attributes of columns.

    Examples:
        table_data = [
            ["name", "score"],
            ["Alex", "86"],
            ["Bob", "88"],
        ]
        html = table_block(table_data, table_attrs={"width": "1"})
    """
    ret = [open_tag("table", table_attrs), open_tag("tbody")]
    for row in rows:
        ret.append(tr_block(row, tr_attrs, td_attrs))
    ret += [close_tag("tbody"), close_tag("table")]
    return "".join(ret)
