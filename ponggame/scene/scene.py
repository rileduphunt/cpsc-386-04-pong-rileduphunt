# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# Module contains scene data structure.
#


"""Contains the scene data structure"""
from pygame import Surface, key
from ponggame import data_dir
from ponggame.entity import Entity
from types import FunctionType
from typing import Dict, List
import os
import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, K_MINUS
from pygame.key import key_code


class Scene:
    """Base scene class that all other scene classes inherit from."""

    def __init__(
        self,
        screen,
        background_color,
        soundtrack=None
    ):

        self._screen: Surface = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._listeners: Dict[int, List[FunctionType]] = {}
        self._is_valid = True
        self._frame_rate = 60
        self._result = 0  # Go to the first output file in the graph.
        self._entities: Dict[str, Entity] = {}

        if soundtrack:
            self._soundtrack = os.path.join(data_dir, soundtrack)
        else:
            self._soundtrack = None
        self._is_soundtrack_on = True

    @property
    def result(self):
        """Return the index indicating the next scene."""
        return 0

    @property
    def is_valid(self) -> bool:
        """Returns true if the scene is currently valid."""
        return self._is_valid

    @property
    def framerate(self):
        return self._frame_rate

    @property
    def next_scene(self) -> str:
        """Returns the string key of the next scene."""
        raise NotImplementedError

    def update(self, delta):
        """Updates the game based on the time delta."""
        pass

    def invalidate(self):
        self._is_valid = False

    def handle_event(self, event):
        if event.type in self._listeners:
            for listener in self._listeners[event.type]:
                listener(event)

    def add_listener(self, event_type: int, listener: FunctionType):
        if event_type in self._listeners.keys():
            self._listeners[event_type].append(listener)
        else:
            self._listeners[event_type] = [listener]

    def draw(self):
        self._screen.blit(self._background, (0, 0))
        for entity in self._entities.values():
            entity.draw(self._screen)

    def start(self):
        """Set up the scene before running it."""
        self._is_valid = True
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1, fade_ms=500)
                pygame.mixer.music.play(-1)
            except pygame.error as pygame_error:
                print(f'Cannot open {self._soundtrack}')
                print(pygame_error)

    def stop(self):
        """Stop the scene."""
        if self._soundtrack:
            pygame.mixer.music.stop()

    def toggle_soundtrack(self):
        self._is_soundtrack_on = not self._is_soundtrack_on
        if not self._is_soundtrack_on:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.play()
