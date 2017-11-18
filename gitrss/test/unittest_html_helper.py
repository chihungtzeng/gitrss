"""
Unit test for html_helper.py
"""

from gitrss.html_helper import escape_html_char
import unittest


class HTMLHelperTest(unittest.TestCase):
    def test_replace_lt_gt(self):
        self.assertEqual("Hello &lt; World",
                         escape_html_char("Hello < World"))
        self.assertEqual("Hello &gt; World",
                         escape_html_char("Hello > World"))


if __name__ == "__main__":
    unittest.main()
