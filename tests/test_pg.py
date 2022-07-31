# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# This is the test file for pg.py
#


"""Tests pg.py to see if it runs."""


import unittest
import pg

class TestPongGame(unittest.TestCase):
    """Test pong game."""
    def test_run(self):
        """Just runs pg.py to see if it executes"""
        pg.main()

if __name__ == '__main__':
    unittest.main()
