"""
Handles high level queries over a git repository.
"""
from __future__ import print_function, absolute_import
import os
import datetime
import git
from rfeed import Item, Feed
from gitrss import shell_util
from gitrss import unified_diff
from gitrss.html_helper import escape_html_char
from gitrss.utf8_utils import to_utf8


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


class GitRepoRSSGenerator(object):
    """
    Generate RSS feeds for a given git reposiotyr.
    """
    def __init__(self, repo_path, repo_name=None):
        if not os.path.isabs(repo_path):
            repo_path = os.path.abspath(repo_path)
        self.repo_path = _detect_repo_basedir(repo_path)

        if repo_name:
            self.repo_name = repo_name
        else:
            _, self.repo_name = os.path.split(self.repo_path)
        self.recent_commits = self.__get_recent_commits()

    def get_repo_name(self):
        """
        Getter.
        """
        return self.repo_name

    def __get_recent_commits(self, num_commits=10):
        """Return the recent NUM_ENTRIES commmits, where NUM_ENTRIES is
        defined in git2rss_setting.
        """
        repo = git.Repo(self.repo_path)
        # We can get info about commits via the elements of |recent_commits|.
        # For example: hexsha, commited_date, author.name, message
        recent_commits = list(repo.iter_commits("master",
                                                max_count=num_commits))
        return recent_commits

    def __get_unified_diff(self, sha1):
        cmd = ["git", "diff", "-U5", sha1 + "^", sha1]
        return shell_util.run_command(cmd, cwd=self.repo_path)

    def __get_feed_item_description(self, commit):
        if commit.parents:
            diff = self.__get_unified_diff(commit.hexsha)
            diff_in_html = unified_diff.GitPatch(diff).format_to_html()
        else:
            diff_in_html = ""
        escaped_msg = escape_html_char(commit.message)
        text = u"<pre>{}</pre>{}".format(escaped_msg, diff_in_html)
        return text

    def __gen_feed_item(self, commit):
        """
        Return a dict that represents an rss entry. See
        data/rss_template.xml for the dict fields.
        """
        feed_item = Item(
            title=commit.message.splitlines()[0],
            author=commit.author.name,
            pubDate=datetime.datetime.fromtimestamp(commit.committed_date),
            description=self.__get_feed_item_description(commit))
        return feed_item

    def to_rss(self):
        """
        Generate rss contents.
        """
        feed_items = [self.__gen_feed_item(_) for _ in self.recent_commits]
        feed = Feed(
            title=self.repo_name,
            link="http://",
            description="Rss entries for {}".format(self.repo_name),
            language="zh-TW",
            lastBuildDate=datetime.datetime.now(),
            items=feed_items)
        return to_utf8(feed.rss())
