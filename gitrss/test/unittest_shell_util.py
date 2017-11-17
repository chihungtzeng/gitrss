# -*- coding: utf-8 -*-
import os
import unittest
import shell_util

class ShellUtilTest(unittest.TestCase):
    def test_run_commmand(self):
        cmd = ["echo", "Hello World"]
        output = shell_util.run_command(cmd)
        self.assertEqual("Hello World\n", output)


if __name__ == "__main__":
    unittest.main()

