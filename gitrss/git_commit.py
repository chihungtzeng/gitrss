# -*- coding: utf-8 -*-
"""
Get git log and unified diff for a given commit.
"""
from __future__ import absolute_import, unicode_literals
import html_helper
import unified_diff
import shell_util
import subprocess
import sys


class GitCommit(object):
    """Use this class to retrive related info regarding a git commit.

    The __init__ method needs a string that identified a commit. The string
    can be a sha1 or "HEAD" etc.
    """
    def __init__(self, sha1):
        self.sha1 = sha1
        self.author = None
        self.commit_date = None
        self.raw_body = None
        self.subject = None
        self.unified_diff = None

    def get_author(self):
        """Return the author of the commit."""
        if not self.author:
            self.author = self._get_git_info(log_format="%aN")
        return self.author

    def get_date(self):
        """Return the date of the commit."""
        if not self.commit_date:
            self.commit_date = self._get_git_info(log_format="%ci")
        return self.commit_date

    def get_raw_body(self):
        """Return the raw body (i.e., commit message) of the commit."""
        if not self.raw_body:
            self.raw_body = self._get_git_info(log_format="%B")
        return self.raw_body

    def get_subject(self):
        """Return the subject of the commit. The subject is the first line
        of the commit message.
        """
        if not self.subject:
            self.subject = self._get_git_info(log_format="%s")
        return self.subject

    def get_unified_diff(self):
        """Return the unified diff for the commit.

        Returns:
            A string of unified diff, with 5 lines preceding and following
            the diff lines in order to give reader the context information.
        """
        if not self.unified_diff:
            cmd = ["git", "diff", "-U5", self.sha1 + "^", self.sha1]
            self.unified_diff = shell_util.run_command(cmd)
        return self.unified_diff

    def _get_git_info(self, log_format=None):
        """Use git command to return the info regarding the commit.

        Args:
            log_format (str): The format asked by git log (see git help log)

        Returns:
            The string returned by git log command. It may contain multiple
            lines.
        """
        cmd = ["git", "log", "-n", "1",
               "--format=\"" + log_format + "\"", self.sha1]
        return shell_util.run_command(cmd)

    def _to_description_list(self):
        """Format the git commit into html description list, that is, <dl>,
        <dt> and <dd> blocks. The layout is:

        Commit: <sha1>
            Author: <author>
            Date: <date>
            Message: <message>
        """
        escaped_msg = html_helper.escape_html_char(self.get_raw_body())

        dcpt = [html_helper.tag_block("dt", "Commit: " + self.sha1),
                html_helper.tag_block("dd", "Author: " + self.get_author()),
                html_helper.tag_block("dd", "Date: " + self.get_date()),
                html_helper.tag_block("dd", "Message: " + escaped_msg), ""]
        return html_helper.tag_block("dl", "\n".join(dcpt))

    def format_to_html(self):
        """Format the git commit with description list and side-by-side diff.
        """
        diff = self.get_unified_diff()
        ret = [self._to_description_list(),
               unified_diff.GitPatch(diff).format_to_html()]
        return "\n".join(ret)

    def to_rss_item(self):
        """
        Return the <item> contents defined by RSS spec. See
            http://www.w3schools.com/xml/xml_rss.asp

        Note:
            The <title>, <link> and <description> are required by the spec.
        """
        escaped_subject = ("<![CDATA[" +
                           html_helper.escape_html_char(self.get_subject()) +
                           "]]>")
        title = html_helper.tag_block("title", escaped_subject)

        link = html_helper.tag_block("link", "file://")

        escaped_subject = html_helper.escape_html_char(self.get_subject())
        description = html_helper.tag_block("description", escaped_subject)

        content = "<![CDATA[" + self.format_to_html() + "]]>"
        content_encoded = html_helper.tag_block("content:encoded",
                                                content)
        item_contents = [title, link, description, content_encoded, ""]
        return html_helper.tag_block("item", "\n".join(item_contents))
