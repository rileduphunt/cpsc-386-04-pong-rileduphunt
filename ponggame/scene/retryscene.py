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

from ponggame.entity import TextDisplay
import pygame
from pygame import Surface, Vector2, mouse
from pygame.event import Event
from ponggame.colors import BLACK, GREEN, RED
from pygame import Rect
from ponggame.scene.scene import Scene


class RetryScene(Scene):
    def __init__(self, screen: Surface):
        super().__init__(screen, (0, 0, 0, 0), soundtrack=None)
        w, h = screen.get_size()
        self._retry_rect = Rect(0, 0, w, h / 2)
        self._retry_text = TextDisplay(
            Vector2(w / 2, h / 4),
            pygame.font.Font(pygame.font.get_default_font(), 40),
            "Play Again"
        )
        self._quit_rect = Rect(0, h / 2, w, h / 2)
        self._quit_text = TextDisplay(
            Vector2(w / 2, 3 * h / 4),
            pygame.font.Font(pygame.font.get_default_font(), 40),
            "Quit"
        )

    def draw(self):
        super().draw()
        pygame.draw.rect(self._screen, GREEN, self._retry_rect)
        pygame.draw.rect(self._screen, RED, self._quit_rect)
        self._retry_text.draw(self._screen)
        self._quit_text.draw(self._screen)

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousepos = mouse.get_pos()
            if self._retry_rect.collidepoint(mousepos):
                print("quit!)")
                self.invalidate(0)
            elif self._quit_rect.collidepoint(mousepos):
                self.invalidate(1)
        super().handle_event(event)
