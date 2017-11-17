#!/usr/bin/python
from gitlog2rss.unified_diff import UnifiedDiffTrunk, UnifiedDiff, GitPatch
from ut_utils import *
import os
import unittest


class UnifiedDiffTrunkTest(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.join(__file__, "..")
        self.tests_dir = os.path.normpath(self.tests_dir)

    def expected_file_name(self, basename, external_css=False):
        if external_css:
            file_name = basename + "-external-css-expect.html"
        else:
            file_name = basename + "-expect.html"
        return os.path.join(self.tests_dir, file_name)

    def read_expected(self, basename, external_css):
        expected_file = self.expected_file_name(basename, external_css)
        return read_file_contents(expected_file)

    def input_file_name(self, basename):
        return os.path.join(self.tests_dir, basename + ".trunk")

    def read_input_trunk(self, basename):
        input_file = self.input_file_name(basename)
        return UnifiedDiffTrunk(read_file_contents(input_file))

    def test_trunk_line_info(self):
        basename = "single"
        udt = self.read_input_trunk(basename)
        lineno_old, len_old, lineno_new, len_new = udt.diff_at()

        self.assertEqual("@@ -30,7 +30,7 @@", udt.line_info())
        self.assertEqual(-30, lineno_old)
        self.assertEqual(7, len_old)
        self.assertEqual(30, lineno_new)
        self.assertEqual(7, len_new)

    def diff_to_html_general(self, basename, external_css):
        udt = self.read_input_trunk(basename)
        expected_file = self.expected_file_name(basename, external_css)
        expected = self.read_expected(basename, external_css)
        html = udt.format_to_html(external_css)
        write_file_if_necessary(expected_file, html)
        self.assertTrue(is_contents_equal(expected, html))

    def test_diff_to_html_oneline(self):
        self.diff_to_html_general("single", False)

    def test_diff_to_html_oneline_external_css(self):
        self.diff_to_html_general("single", True)

    def test_diff_to_html_multiline(self):
        self.diff_to_html_general("multiline-diff", False)

    def test_diff_to_html_multiline_external_css(self):
        self.diff_to_html_general("multiline-diff", True)

    def test_diff_to_html_multiline2(self):
        self.diff_to_html_general("multiline-diff2", False)


class UnifiedDiffTest(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.join(__file__, "..")
        self.tests_dir = os.path.normpath(self.tests_dir)

    def test_file_name_retrival(self):
        input_file = os.path.join(self.tests_dir, "single-trunk.patch")
        ud = UnifiedDiff(read_file_contents(input_file))
        self.assertEqual("src/eval_env.cc", ud.get_file_name())

    def test_added_file(self):
        patch = """diff --git a/tests/multi-trunk-expect.html b/tests/multi-trunk-expect.html
new file mode 100644
index 0000000..7ec01c2
--- /dev/null
+++ b/tests/multi-trunk-expect.html
@@ -0,0 +1,413 @@
"""
        file_name = UnifiedDiff(patch).get_file_name()
        self.assertEqual("tests/multi-trunk-expect.html", file_name)

    def cmp_general(self, input_file, expected_file):
        ud = UnifiedDiff(read_file_contents(input_file))
        expected = read_file_contents(expected_file)
        html = ud.format_to_html()
        write_file_if_necessary(expected_file, html)
        self.assertEqual(expected, html)

    def test_unified_diff_to_html(self):
        input_file = os.path.join(self.tests_dir, "single-trunk.patch")
        expected_file = os.path.join(self.tests_dir,
                                     "single-trunk-ud-expect.html")
        self.cmp_general(input_file, expected_file)

    def test_unified_diff_to_html2(self):
        input_file = os.path.join(self.tests_dir, "multi-trunk.patch")
        expected_file = os.path.join(self.tests_dir,
                                     "multi-trunk-expect.html")
        self.cmp_general(input_file, expected_file)


class GitPatchTest(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.join(__file__, "..")
        self.tests_dir = os.path.normpath(self.tests_dir)

    def test_split(self):
        input_file = os.path.join(self.tests_dir, "single-trunk.patch")
        contents = read_file_contents(input_file)
        patches = GitPatch(contents).split()
        self.assertEqual(contents, patches[0])

    def cmp_general(self, input_file, expected_file):
        gpt = GitPatch(read_file_contents(input_file))
        expected = read_file_contents(expected_file)
        html = gpt.format_to_html()
        write_file_if_necessary(expected_file, html)
        self.assertEqual(expected, html)

    def test_format_to_html(self):
        input_file = os.path.join(self.tests_dir, "11e9fc4.patch")
        expected_file = os.path.join(self.tests_dir, "11e9fc4.html")
        self.cmp_general(input_file, expected_file)


if __name__ == "__main__":
    unittest.main()
