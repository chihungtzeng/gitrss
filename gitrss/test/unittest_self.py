# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from gitrss import GitRepo
import os
import pprint
import shutil
import unittest


class GitRepoTest(unittest.TestCase):
    def setUp(self):
        repo_path = os.path.normpath(os.path.join(__file__, ".."))
        self.git_repo = GitRepo(repo_path)

    def test_repo_name(self):
        self.assertEqual("gitrss", self.git_repo.get_repo_name())

    def test_get_unified_diff(self):
        sha1 = self.git_repo.recent_commits[0].hexsha
        diff = self.git_repo.get_unified_diff(sha1)
        self.assertTrue(diff.startswith("diff"))


if __name__ == "__main__":
    unittest.main()
