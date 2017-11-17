"""
Handle Unified diff and produce html.
"""

from __future__ import print_function
import html_helper
import re
import sys


class UnifiedDiffTrunk(object):
    """A trunk starts at @@ from-file-line-numbers to-file-line-numbers @@
    """
    def __init__(self, trunk):
        if isinstance(trunk, list):
            self.trunk = trunk
        elif isinstance(trunk, basestring):
            self.trunk = trunk.splitlines()
        else:
            print("trunk should be a str or list")
            sys.exit(1)

    def line_info(self):
        """
        Return: the line info with heading and trailing @@
        @@ from-file-line-numbers to-file-line-numbers @@
        """
        reg = re.compile(r"(?P<chunk_header>@@ .* @@)")
        for line in self.trunk:
            match = reg.match(line)
            if match:
                return match.expand(r"\g<chunk_header>")
        return ""

    def diff_at(self):
        """
        Returns:
        A 4-tuple that indicates the diff position.

        On failure, it returns -1, -1, -1, -1
        """
        line_pos = r"[" + re.escape("+-") + r"]\d+"
        reg = re.compile((r"@@ (?P<lineno_old>%s),(?P<len_old>\d+) "
                          r"(?P<lineno_new>%s),(?P<len_new>\d+) @@"
                          % (line_pos, line_pos)))
        lineno_old, len_old, lineno_new, len_new = -1, -1, -1, -1
        match = reg.match(self.line_info())
        if match:
            lineno_old = int(match.expand(r"\g<lineno_old>"))
            len_old = int(match.expand(r"\g<len_old>"))
            lineno_new = int(match.expand(r"\g<lineno_new>"))
            len_new = int(match.expand(r"\g<len_new>"))
        return lineno_old, len_old, lineno_new, len_new

    def format_to_html(self, external_css=False):
        """Format the trunk in the html format
        """
        if external_css:
            return self._format_to_html_external_css()
        else:
            return self._format_to_html_inline_css()

    def _format_to_html_external_css(self):
        """Produce html with external css style, two-side layout.

        Note: Users need to supply his/her css file, where the following
              class are defined:

              ud_table: Table style.
              ud_lineno: Line number style.
              ud_neutral: The style for unchanged lines.
              ud_minus: The style for deleted lines in the old revision.
              ud_plus: The style for added lines in the new revision.
        """
        table_attrs = {"class": "ud_table"}
        lineno_attrs = {"class": "ud_lineno"}
        plus_attrs = {"class": "ud_plus"}
        minus_attrs = {"class": "ud_minus"}
        neutral_attrs = {"class": "ud_neutral"}
        return self._format_to_html_general(table_attrs, lineno_attrs,
                                            neutral_attrs, minus_attrs,
                                            plus_attrs)

    def _format_to_html_inline_css(self):
        """Produce html with inline css style, two-side layout.

        Example:
            - printf("Hello World"); + printf("Hello Kitty");
        """
        table_attrs = {
            "border": "0",
            "width": "100%",
            "style": ("white-space: pre-wrap; "
                      "border-collapse: collapse; "
                      "font-family: Courier New, Courier, monospace;")}
        lineno_attrs = {"style": ("background-color: lightgray; "
                                  "vertical-align: top; "
                                  "text-align: right; ")}
        neutral_attrs = {"style": ("background-color: inherit; "
                                   "vertical-align: top; "
                                   "width:47% ")}
        minus_attrs = {"style": ("background-color: pink; "
                                 "vertical-align: top; "
                                 "width:47%")}
        plus_attrs = {"style": ("background-color: yellowgreen; "
                                "vertical-align: top; "
                                "width:47%")}

        return self._format_to_html_general(table_attrs, lineno_attrs,
                                            neutral_attrs, minus_attrs,
                                            plus_attrs)

    def _format_to_html_general(self, table_attrs, lineno_attrs,
                                neutral_attrs, minus_attrs, plus_attrs):
        """General method to produce diff table. The css styles are given by
        callers.
        """
        lineno_old, len_old, lineno_new, len_new = self.diff_at()
        lineno_old = abs(lineno_old)
        lineno_new = abs(lineno_new)
        rows = [["<td>  </td>" for _ in range(4)]
                for _ in range(max(len_old, len_new)+1)]
        row_old = 0
        row_new = 0

        for line in self.trunk:
            tline = html_helper.escape_html_char(line)
            lblock_old = html_helper.td_block(str(lineno_old), lineno_attrs)
            lblock_new = html_helper.td_block(str(lineno_new), lineno_attrs)
            if max(row_old, row_new) == len(rows):
                rows.append(["<td></td>" for _ in range(4)])
            if len(line) <= 0:
                pass
            elif line[0] == " ":
                row_old = max(row_old, row_new)
                row_new = row_old
                tblock = html_helper.td_block([tline], neutral_attrs)
                rows[row_old][0] = lblock_old
                rows[row_old][1] = tblock
                rows[row_new][2] = lblock_new
                rows[row_new][3] = tblock
                lineno_old += 1
                lineno_new += 1
                row_old += 1
                row_new += 1
            elif line[0] == "-":
                tblock = html_helper.td_block([tline], minus_attrs)
                rows[row_old][0] = lblock_old
                rows[row_old][1] = tblock
                lineno_old += 1
                row_old += 1
            elif line[0] == "+":
                tblock = html_helper.td_block([tline], plus_attrs)
                rows[row_new][2] = lblock_new
                rows[row_new][3] = tblock
                lineno_new += 1
                row_new += 1
        # For an added file, the two columns to the left are empty td blcks.
        # It makes the column width not consistent with other tables. The
        # same happens for a deleted file. Therefore we make an empty row
        # with proper attributes.
        if row_old == 0 or row_new == 0:
            rows.append([html_helper.td_block("  "),
                         html_helper.td_block("", neutral_attrs),
                         html_helper.td_block("  "),
                         html_helper.td_block("", neutral_attrs)])

        html = [html_helper.tag_block("div", self.line_info()),
                html_helper.open_tag("table", table_attrs),
                html_helper.open_tag("tbody")]
        for row in rows:
            html += [html_helper.open_tag("tr"), "".join(row),
                     html_helper.close_tag("tr")]
        html += [html_helper.close_tag("tbody"),
                 html_helper.close_tag("table"),
                 ""]
        return "\n".join(html)


class UnifiedDiff(object):
    """
    Helper class for dealing with unified diff format. The format is as
    follows.

    @@ from-file-line-numbers to-file-line-numbers @@
      line-from-either-file
      line-from-either-file...

    The lines common to both files begin with a space character. The lines
    that actually differ between the two files have one of the following
    indicator characters in the left print column:
    +
    A line was added here to the first file.
    -
    A line was removed here from the first file.

    Note:
        This helper class handles the diff of *ONE* file. For a diff that
        contains multiple files (i.e., a git commit), refer to GitPatch
        class.
    """
    def __init__(self, diff):
        if isinstance(diff, basestring):
            self.diff = diff.splitlines()
        elif isinstance(diff, list):
            self.diff = diff
        else:
            print("Invalid args, diff should be str of list.")
            sys.exit(1)

    def get_file_name(self):
        """Return the filename that the diff comes from."""
        return self._parse_file_name()

    def _parse_file_name(self):
        """
        Returns:
        The file name of the unified diff. We scan the following pattern.
        --- a/src/eval_env.cc
        +++ b/src/eval_env.cc
        """
        regs = [re.compile("%s (?P<file_name>.+)" % (re.escape("+++"))),
                re.compile("%s (?P<file_name>.+)" % (re.escape("+++")))]
        file_names = ["", ""]
        for line in self.diff:
            for index in range(2):
                match = regs[index].match(line)
                if match:
                    file_names[index] = match.expand(r"\g<file_name>")
        if file_names[0] != "/dev/null":
            return file_names[0][2:]
        else:
            return file_names[1][2:]
        return None

    def _get_trunks(self):
        """Split self.diff into unified diff trunks and return them in a
        list.
        """
        ret = []
        trunk = []

        # The first 4 lines should be skiped. They are
        #
        # diff --git a/unified_diff_ut.py b/unified_diff_ut.py
        # index a3be2ff..c1d8bb4 100644
        # --- a/unified_diff_ut.py
        # +++ b/unified_diff_ut.py
        start_trunk = False
        for line in self.diff:
            if len(line) == 0:
                continue
            elif line[0] == "@":
                # A new trunk
                start_trunk = True
                if trunk:
                    ret.append("\n".join(trunk))
                trunk = [line]
            else:
                if start_trunk:
                    trunk.append(line)
        if trunk:
            ret.append("\n".join(trunk))
        return ret

    def format_to_html(self):
        """Return the diff table (in html)"""
        html = [html_helper.tag_block("h2", self.get_file_name())]
        trunks = self._get_trunks()
        for trunk in trunks:
            snippet = UnifiedDiffTrunk(trunk).format_to_html()
            html.append(snippet)
        return "\n".join(html)


class GitPatch(object):
    """Handles a complete git diff.
    """
    def __init__(self, patch):
        if isinstance(patch, basestring):
            self.patch = patch.splitlines()
        else:
            self.patch = patch

    def split(self):
        """
        Split self.patch into multiple, one-file patches.
        """
        ret = []
        reg = re.compile("diff --git .+")
        patch = []
        for line in self.patch:
            match = reg.match(line)
            if match:
                if patch:
                    ret.append("\n".join(patch))
                patch = [line]
            else:
                patch.append(line)
        if patch:
            patch.append("")  # ensure the last char is \n.
            ret.append("\n".join(patch))
        return ret

    def format_to_html(self):
        """Format a complete git diff into side-by-side comparison table.
        """
        patches = self.split()
        result = []
        for patch in patches:
            html = UnifiedDiff(patch).format_to_html()
            result.append(html)
        return "\n".join(result)
