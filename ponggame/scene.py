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
from ponggame import colors
import pygame

class Scene:
    def __init__(self, screen, background_color):
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._is_valid = True
        self._frame_rate = 60

    @property
    def is_valid(self):
        return self._is_valid

    @property
    def framerate(self):
        return self._frame_rate

    @property
    def next_scene(self) -> str:
        """Returns the string key of the next scene."""
        return ""

    def update(self):
        pass

    def handle_event(self, event):
        if (event.type == pygame.KEYDOWN and \
            event.key == pygame.K_ESCAPE) or \
            event.type == pygame.QUIT:
            self._is_valid = False

    def draw(self):
        self._screen.blit(self._background, (0,0))

class TitleScene(Scene):
    def __init__(self, screen, background_color, title,):
        super().__init__(screen, background_color=background_color)
        self._title = title
        (w,h) = self._screen.get_size()
        title_font = pygame.font.Font(pygame.font.get_default_font(),36)
        self._rendered_title = title_font.render(self._title, True, (0,0,0))
        self._title_position = self._rendered_title.get_rect(center=(w/2,h/2))

    def draw(self):
        super().draw()
        self._screen.blit(self._rendered_title, self._title_position)



class GameScene(Scene):
    def __init__(self, screen, background_color):
        super().__init__(screen, background_color)
        self._frame_rate = 1
    def update(self):
        print("I am the game scene")
