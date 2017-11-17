# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import unittest
from gitlog2rss.git_commit import GitCommit
from ut_utils import read_file_contents, write_file_if_necessary


class GitObjectTest(unittest.TestCase):
    def setUp(self):
        self.gc = GitCommit("HEAD")

        self.tests_dir = os.path.join(__file__, "..")
        self.tests_dir = os.path.normpath(self.tests_dir)

    def test_get_author(self):
        ret = self.gc.get_author()
        self.assertIsInstance(ret, basestring)
        self.assertNotEqual("", ret)

    def test_get_date(self):
        ret = self.gc.get_date()
        self.assertIsInstance(ret, basestring)
        self.assertNotEqual("", ret)

    def test_get_raw_body(self):
        ret = self.gc.get_raw_body()
        self.assertIsInstance(ret, basestring)
        self.assertNotEqual("", ret)

    def test_get_subject(self):
        ret = self.gc.get_subject()
        self.assertIsInstance(ret, basestring)
        self.assertNotEqual("", ret)

    def test_get_unified_diff(self):
        ret = self.gc.get_unified_diff()
        self.assertIsInstance(ret, basestring)
        self.assertNotEqual("", ret)

    def test_description_list(self):
        html = self.gc.format_to_html()
        self.assertNotEqual("", html)

    def test_6ee1804(self):
        sha1 = "6ee1804"
        html = GitCommit(sha1).format_to_html()
        expected_file = os.path.join(self.tests_dir, sha1 + "-expect.html")
        expected = read_file_contents(expected_file)
        write_file_if_necessary(expected_file, html)
        self.assertEqual(expected, html)

    def test_xml_item(self):
        sha1 = "6ee1804"
        item_block = GitCommit(sha1).to_rss_item()
        self.assertTrue("<title>" in item_block)
        self.assertTrue("</title>" in item_block)
        self.assertTrue("<link>" in item_block)
        self.assertTrue("</link>" in item_block)
        self.assertTrue("<description>" in item_block)
        self.assertTrue("</description>" in item_block)

if __name__ == "__main__":
    unittest.main()
