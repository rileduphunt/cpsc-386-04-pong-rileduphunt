#! /usr/bin/env python3
# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# This is the entry point to my Pong program.
#


"""This module is the entry point to Pong."""


import sys
from ponggame import game


def main():
    """Entry point of Pong game."""
    the_game_obj = game.Game(sys.argv)
    the_game_obj.build_scenegraph()
    the_game_obj.run()

if __name__ == '__main__':
    main()
