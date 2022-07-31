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
import pygame
from ponggame import colors


class Scene:
    """Base scene class that all other scene classes inherit from."""

    def __init__(self, screen, background_color):
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._is_valid = True
        self._frame_rate = 1
        self._result = 0

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
        return ""

    def update(self, delta):
        """Placeholder: Updates the game based on the time delta."""

    def handle_event(self, event):
        if (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ) or event.type == pygame.QUIT:
            self._is_valid = False
            self._is_valid = False

    def draw(self):
        self._screen.blit(self._background, (0, 0))

    def reset(self):
        """Reset the scene before loading it again."""
        self._is_valid = True


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


class GameScene(Scene):
    """Scene that manages the actual game"""

    def update(self, delta):
        print("I am the game scene")
