# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import pprint
import shutil
import unittest
from gitrss import GitRepoRSSGenerator


class GitRepoTest(unittest.TestCase):
    def setUp(self):
        repo_path = os.path.normpath(os.path.join(__file__, ".."))
        self.genr = GitRepoRSSGenerator(repo_path)

    def test_repo_name(self):
        self.assertEqual("gitrss", self.genr.get_repo_name())


if __name__ == "__main__":
    unittest.main()
