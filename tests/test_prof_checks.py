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


import unittest
import format_check
import header_check
import lint_check

class TestProfChecks(unittest.TestCase):
    """Test the program using the professor's checks."""
    def test_header(self):
        """Checks headers."""
        try:
            header_check.main()
        except SystemExit as exception:
            print(exception)

    def test_lint(self):
        """Check linting"""
        try:
            lint_check.main()
        except SystemExit as exception:
            print(exception)
    def test_format(self):
        """Checks formatting"""
        try:
            format_check.main()
        except SystemExit as exception:
            print(exception)


if __name__ == '__main__':
    unittest.main()
