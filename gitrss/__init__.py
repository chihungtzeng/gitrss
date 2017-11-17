"""
Handles high level queries over a git repository.
"""
from __future__ import print_function, absolute_import
import os
import time
import git
from jinja2 import Template
from . import shell_util
from . import html_helper
from . import unified_diff
from .git_commit import GitCommit


def _detect_repo_basedir(repo_path):
    """
    Return the base path of a git repository. That is, the path that
    contains .git subdirectory.
    """
    dir_chains = repo_path.split(os.sep)
    while dir_chains:
        candidate = os.sep.join(dir_chains)
        path = os.path.join(candidate, ".git")
        if os.path.isdir(path):
            return candidate
        else:
            dir_chains.pop()
    raise ValueError("Not a valid git repo: {}".format(repo_path))


class GitRepo(object):
    def __init__(self, repo_path, repo_name=None):
        if not os.path.isabs(repo_path):
            repo_path = os.path.abspath(repo_path)
        self.repo_path = _detect_repo_basedir(repo_path)

        if repo_name:
            self.repo_name = repo_name
        else:
            _, self.repo_name = os.path.split(self.repo_path)
        self.recent_commits = self._get_recent_commits()

    def get_repo_name(self):
        """
        Getter.
        """
        return self.repo_name

    def _get_recent_commits(self, num_commits=10):
        """Return the recent NUM_ENTRIES commmits, where NUM_ENTRIES is
        defined in git2rss_setting.
        """
        repo = git.Repo(self.repo_path)
        # We can get info about commits via the elements of |recent_commits|.
        # For example: hexsha, commited_date, author.name, message
        recent_commits = list(repo.iter_commits("master",
                                                max_count=num_commits))
        return recent_commits

    def get_unified_diff(self, sha1):
        cmd = ["git", "diff", "-U5", sha1 + "^", sha1]
        return shell_util.run_command(cmd, cwd=self.repo_path)

    def _get_subject(self, message):
        """
        Return the subject of the commit. The subject is the first line of
        the commit message.
        """
        return message.splitlines()[0]

    def _get_rss_entry(self, commit):
        """
        Return a dict that represents an rss entry. See
        data/rss_template.xml for the dict fields.
        """
        escape = html_helper.escape_html_char
        entry = {}
        entry["title"] = escape(self._get_subject(commit.message))

        entry["link"] = "http://"

        # title, description, and content:encoded are wrapped by CDATA
        # so we don't need to escape html chars.
        date = time.asctime(time.gmtime(commit.committed_date))
        description = (u"<p>Commit: " + commit.hexsha + "</p>"
                       u"<p>Author: " + commit.author.name + "</p>"
                       u"<p>Date: " + date + "</p>")
        entry["description"] = description
        diff = self.get_unified_diff(commit.hexsha)
        entry["content"] = unified_diff.GitPatch(diff).format_to_html()
        return entry

    def to_rss(self):
        """
        Generate rss contents.
        """
        channel = {
            "title": self.repo_name,
            "link": "file://",
            "description": "Rss entries for {}".format(self.repo_name)
        }
        entries = []
        for commit in self.recent_commits:
            entries.append(self._get_rss_entry(commit))

        return html_helper.gen_rss_contents(channel, entries)
