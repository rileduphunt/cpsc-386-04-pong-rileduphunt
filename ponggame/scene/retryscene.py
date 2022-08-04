# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# Contains the retryscene data structure.
#

from ponggame.scene.scene import Scene


class RetryScene(Scene):
    def __init__(self, screen, background_color):
        super().__init__(screen, background_color, soundtrack=None)
