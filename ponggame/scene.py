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
from pygame import Rect, Surface
from pygame.event import Event
from ponggame.entity import Ball, Entity, Goal, Paddle, Wall
from types import FunctionType
from typing import Dict, List
import pygame
from pygame.constants import KEYDOWN, K_ESCAPE
from pygame.key import key_code
from ponggame import colors


class Scene:
    """Base scene class that all other scene classes inherit from."""

    def __init__(self, screen, background_color):
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._registered_events: Dict[int, List[FunctionType]] = {}
        self._is_valid = True
        self._frame_rate = 60
        self._result = 0
        self._entities: Dict[str, Entity] = {}

        def quit(event):
            if event.key == pygame.K_ESCAPE:
                self.invalidate()

        self.register_eventhandler(pygame.KEYDOWN, quit)

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
        if event.type in self._registered_events:
            for handler in self._registered_events[event.type]:
                handler(event)

    def register_eventhandler(self, event_type: int, handler: FunctionType):
        if event_type in self._registered_events:
            self._registered_events[event_type].append(handler)
        else:
            self._registered_events[event_type] = [handler]

    def draw(self):
        self._screen.blit(self._background, (0, 0))

    def start(self):
        """Set up the scene before running it."""
        self._is_valid = True

    def stop(self):
        """Stop the scene."""
        pass


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
    def __init__(self, screen: Surface, background_color):
        super().__init__(screen, background_color)
        w, h = screen.get_size()
        ball_height = 25
        goal_width = 1
        goal_offset = ball_height*2.5 + goal_width
        self._entities['ball'] = Ball((w/2, h/2), 25, colors.WHITE)
        self._entities['topwall'] = Wall(Rect(0, 0, w, 10))
        self._entities['bottomwall'] = Wall(Rect(0, 790, w, 10))
        self._entities['player_goal'] = Goal(
            Rect(0 - goal_offset, -h, goal_width, h * 3)
        )
        self._entities['enemy_goal'] = Goal(
            Rect(w + goal_offset, -h, goal_width, h * 3)
        )
        self._entities['player_paddle'] = Paddle((30, h / 2))
        self._entities['enemy_paddle'] = Paddle((w-30, h / 2))

        def paddle_move(event: Event):
            if event.key == pygame.K_UP:
                self._entities['player_paddle']._acceleration.y -= 1/60
            elif event.key == pygame.K_DOWN:
                self._entities['player_paddle']._acceleration.y += 1/60

        def paddle_stop(event: Event):
            if event.key == pygame.K_UP:
                self._entities['player_paddle']._velocity.y *= 0
                self._entities['player_paddle']._acceleration *= 0
            elif event.key == pygame.K_DOWN:
                self._entities['player_paddle']._velocity.y *= 0
                self._entities['player_paddle']._acceleration *= 0

        def restart(event: Event):
            if event.key == pygame.K_SPACE:
                ball = self._entities['ball']
                if not ball.is_moving:
                    ball.reset()
                    ball.start()

        self.register_eventhandler(pygame.KEYDOWN, restart)
        self.register_eventhandler(pygame.KEYDOWN, paddle_move)
        self.register_eventhandler(pygame.KEYUP, paddle_stop)

    def update(self, delta):
        self.collide_entities(delta)
        for name in self._entities:
            self._entities[name].update(delta, self._entities)

    def draw(self):
        super().draw()
        for name in self._entities:
            self._entities[name].draw(self._screen)

    def collide_entities(self, delta):
        checked = []
        for first in self._entities.values():
            for second in self._entities.values():
                if (
                    first is not second and
                    first not in checked and
                    second not in checked and
                    first.collision_rect.colliderect(second.collision_rect)
                ):
                    first.collide(delta, second)
                    second.collide(delta, first)
                else:
                    pass
            checked.append(first)
