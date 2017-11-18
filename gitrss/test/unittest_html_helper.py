"""
Unit test for html_helper.py
"""

from gitrss.html_helper import (escape_html_char, gen_rss_contents)
import unittest


class HTMLHelperTest(unittest.TestCase):
    def test_replace_lt_gt(self):
        self.assertEqual("Hello &lt; World",
                         escape_html_char("Hello < World"))
        self.assertEqual("Hello &gt; World",
                         escape_html_char("Hello > World"))

    def test_gen_rss_contents(self):
        channel = {
            "title": "Channel title",
            "link": "file://",
            "description": "Channel description"}
        entries = [
            {"title": "title0",
             "link": "link0",
             "description": "description0",
             "content": "content0"},
            {"title": "title1",
             "link": "link1",
             "description": "a + b = c",
             "content": "content1"},
        ]
        ret = gen_rss_contents(channel, entries)
        self.assertTrue("<item>" in ret)


if __name__ == "__main__":
    unittest.main()
