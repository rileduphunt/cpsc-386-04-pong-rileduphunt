# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# Contains titlescene data structure.
#


"""Contains the scene data structure"""
from os import error
from pygame import Rect, Surface
from pygame.event import Event
from ponggame.entity import Ball, Entity, Goal, Paddle, Wall
from types import FunctionType
from typing import Dict, List
import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, K_MINUS
from pygame.key import key_code
from ponggame import colors
from ponggame.scene.scene import Scene


class TitleScene(Scene):
    def __init__(self, screen, background_color, title):
        super().__init__(screen, background_color=background_color)
        self._title = title
        (w, h) = self._screen.get_size()
        title_font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._rendered_title = title_font.render(
            self._title, True, colors.BLACK
        )
        self._title_position = self._rendered_title.get_rect(
            center=(w / 2, h / 2)
        )

    def draw(self):
        super().draw()
        self._screen.blit(self._rendered_title, self._title_position)
