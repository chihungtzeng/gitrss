# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from gitlog2rss import GitRepo
import os
import pprint
import shutil
import unittest


class GitRepoTest(unittest.TestCase):
    def setUp(self):
        repo_path = os.path.normpath(os.path.join(__file__, ".."))
        self.git_repo = GitRepo(repo_path)

    def test_repo_name(self):
        self.assertEqual("gitlog2rss", self.git_repo.get_repo_name())

    def test_get_unified_diff(self):
        sha1 = self.git_repo.recent_commits[0].hexsha
        diff = self.git_repo.get_unified_diff(sha1)
        self.assertTrue(diff.startswith("diff"))

    def test__get_rss_entry(self):
        commit = self.git_repo.recent_commits[0]
        entry = self.git_repo._get_rss_entry(commit)
        self.assertEqual(4, len(entry))


if __name__ == "__main__":
    unittest.main()
