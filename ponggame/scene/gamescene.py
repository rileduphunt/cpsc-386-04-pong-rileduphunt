# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# Contains gamescene data structure.
#


"""Contains the scene data structure"""
from os import error

from pygame.font import Font
import ponggame
from ponggame.scene.scene import Scene
from pygame import Rect, Surface, Vector2
from pygame.event import Event
from ponggame.entity import Ball, Goal, Paddle, TextDisplay, Wall
from typing import Dict, List
import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, K_MINUS, USEREVENT
from pygame.key import key_code
from ponggame import colors
from ponggame.scene.scene import Scene


class GameScene(Scene):
    """Scene that manages the actual game"""
    def __init__(self, screen: Surface, background_color, soundtrack):
        super().__init__(screen, background_color, soundtrack)
        self.gamespeed = 1
        w, h = screen.get_size()
        ball_height = 25
        goal_width = 1
        goal_offset = ball_height * 2.5 + goal_width
        self._player_score = 0
        self._opponent_score = 0
        self._entities['ball'] = Ball((w/2, h/2), colors.WHITE)
        ball = self._entities['ball']
        self._entities['topwall'] = Wall(Rect(0, 0, w, 10))
        self._entities['bottomwall'] = Wall(Rect(0, 790, w, 10))
        self._entities['player_goal'] = Goal(
            Rect(0 - goal_offset, -h, goal_width, h * 3)
        )
        self._entities['opponent_goal'] = Goal(
            Rect(w + goal_offset, -h, goal_width, h * 3)
        )
        self._entities['player_paddle'] = Paddle((30, h / 2))
        self._entities['opponent_paddle'] = Paddle((w-30, h / 2))
        font = Font(pygame.font.get_default_font(), 35)

        self._entities['player_score'] = TextDisplay(
            position=Vector2(w/3, h/9),
            font=font,
            text="0",
        )
        self._entities['opponent_score'] = TextDisplay(
            position=Vector2(2*w/3, h/9),
            font=font,
            text="0",
        )

        def paddle_move(event: Event):
            if event.key == pygame.K_UP:
                self._entities['player_paddle']._acceleration.y = -1/60
            elif event.key == pygame.K_DOWN:
                self._entities['player_paddle']._acceleration.y += 1/60
            elif event.key == pygame.K_w:
                self._entities['player_paddle']._acceleration.y = -1/60
            elif event.key == pygame.K_s:
                self._entities['player_paddle']._acceleration.y = 1/60

        def paddle_stop(event: Event):
            if event.key == pygame.K_UP:
                self._entities['player_paddle']._velocity.y *= 0
                self._entities['player_paddle']._acceleration *= 0
            elif event.key == pygame.K_DOWN:
                self._entities['player_paddle']._velocity.y *= 0
                self._entities['player_paddle']._acceleration *= 0
            elif event.key == pygame.K_w:
                self._entities['player_paddle']._velocity.y *= 0
                self._entities['player_paddle']._acceleration *= 0
            elif event.key == pygame.K_s:
                self._entities['player_paddle']._velocity.y *= 0
                self._entities['player_paddle']._acceleration *= 0

        def restart(event: Event):
            ball.reset()
            ball.start()

        def score_point(ball: Ball, delta: int, goal: Goal):
            if ball is ball and isinstance(goal, Goal):
                if goal is self._entities['player_goal']:
                    print("The opponent scores")
                    self._opponent_score += 1
                elif goal is self._entities['opponent_goal']:
                    print("The player scores")
                    self._player_score += 1
                self._entities['player_score'].text = str(self._player_score)
                self._entities['opponent_score'].text = str(
                    self._opponent_score
                    )
                ball.reset()
                ball.start_timer()

        self.add_listener(USEREVENT+1, ball.make_color(colors.RED))
        self.add_listener(USEREVENT+2, ball.make_color(colors.YELLOW))
        self.add_listener(USEREVENT+3, ball.make_color(colors.GREEN))
        self.add_listener(USEREVENT+4, ball.make_color(colors.WHITE))

        ball.add_listener('collide', score_point)
        self.add_listener(USEREVENT+4, restart)
        self.add_listener(pygame.KEYDOWN, paddle_move)
        self.add_listener(pygame.KEYUP, paddle_stop)

    def update(self, delta):
        self.collide_entities(delta)
        for name in self._entities:
            self._entities[name].update(delta, self._entities)
        if self._player_score >= 3:
            self.invalidate()
        elif self._opponent_score >= 3:
            self.invalidate()

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

    def start(self):
        super().start()
        self._entities['ball'].start_timer()
        self._player_score = 0
        self._opponent_score = 0
