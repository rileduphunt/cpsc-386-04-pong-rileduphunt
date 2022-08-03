# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# This tests the program using the professor's tests.
#


"""Tests the program using the professor's checks."""


import sys
import unittest
import format_check
import header_check
import lint_check

class TestProfChecks(unittest.TestCase):
    """
    Test the program using the professor's checks.
    Must add files from .actions to the sitepackages folder in
    your virtual environment.
    e.g. ln -s .actions/*.py env/lib/python3.0/site-packages/
    """

    def setUp(self) -> None:
        sys.argv.append('.')
        sys.argv.append('ponggame')
        sys.argv.append('ponggame/scene')

    def test_header(self):
        """Checks headers."""
        try:
            header_check.main()
        except SystemExit as exception:
            self.assertEqual(exception.code, 0)

    def test_lint(self):
        """Check linting"""
        try:
            lint_check.main()
        except SystemExit as exception:
            self.assertEqual(exception.code, 0)


    def test_format(self):
        """Checks formatting"""
        try:
            format_check.main()
        except SystemExit as exception:
            self.assertEqual(exception.code, 0)



if __name__ == '__main__':
    unittest.main()
