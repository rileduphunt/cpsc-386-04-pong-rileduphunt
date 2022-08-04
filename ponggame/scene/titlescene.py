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
from pygame import Rect, Surface, Vector2
from pygame.event import Event
from ponggame.entity import Ball, Entity, Goal, Paddle, TextDisplay, Wall
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
        pos = Vector2(w / 2, h / 2)
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text = ("HOW TO PLAY:\n"
                "Control the left paddle with the up and down keys.\n"
                "Try to keep the ball out of your opponent's goal.\n"
                "The first player to score 3 points wins!\n")
        self._entities['title'] = TextDisplay(pos, font, text)
        self.add_listener(pygame.KEYDOWN, lambda event: self.invalidate())

    def handle_event(self, event):
        super().handle_event(event)
