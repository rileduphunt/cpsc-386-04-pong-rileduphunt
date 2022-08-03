# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# This is the __init__ file for the ponggame module.
#


"""__init__ for ponggame module."""

import os


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'assets/')
__all__ = ['game', 'colors', 'scene', 'data_dir']
