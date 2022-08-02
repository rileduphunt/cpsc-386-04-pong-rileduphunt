# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# Entity class for an entity component system.
#


"""Module containing classes of entities"""


from decimal import Decimal
from os import environ
from ponggame import colors
from typing import Protocol, Tuple
from pygame import Rect, Vector2, Surface
from random import randrange
import pygame.gfxdraw


class Entity():
    def __init__(self, position: Vector2, dimensions: Vector2) -> None:
        self._initial_position = Vector2(position)
        self._position = self._initial_position
        self._listeners = {}
        self._dimensions = dimensions
        self._rect = Rect(
            self._position - (dimensions / 2),
            dimensions
        )

    def update(self, delta, environment):
        pass

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, colors.RED, self.collision_rect)

    @property
    def listeners(self):
        return self._listeners

    @property
    def collision_rect(self):
        return Rect(
            self._position - (self._dimensions / 2),
            self._dimensions
        )

    def collide(self, delta, entity):
        pass


class Ball(Entity):
    default_radius = 25

    def __init__(self, position: Vector2, radius: float, color: Tuple) -> None:
        super().__init__(position, Vector2(2 * radius, 2 * radius))
        self._velocity = Vector2(0, 0)
        self.radius = Ball.default_radius
        self.color = color

    def update(self, delta: float, environment):
        """Updates the ball each tick."""
        self._position = self._position + self._velocity * delta

    def draw(self, surface: Surface):
        """Draws the ball."""
        pygame.gfxdraw.aacircle(
            surface,
            round(self._position.x),
            round(self._position.y),
            round(self.radius),
            self.color
        )
        pygame.gfxdraw.filled_circle(
            surface,
            round(self._position.x),
            round(self._position.y),
            round(self.radius),
            self.color
        )

    def start(self):
        """Starts the ball in a mostly random direction"""
        self._velocity = Vector2(Ball.default_radius / 60)
        self._velocity.rotate_ip(randrange(1, 90))
        self._velocity.rotate_ip(90 * randrange(4))
        # self._velocity = Vector2(0, -25/60)

    def stop(self):
        self._velocity = self._velocity * 0

    @property
    def is_moving(self):
        return self._velocity.length_squared() != 0.0

    def collide(self, delta, entity: Entity):
        self._position -= self._velocity * delta
        if isinstance(entity, Wall):
            self._velocity.y = -self._velocity.y
        elif isinstance(entity, Paddle):
            self._velocity.x = -self._velocity.x
        elif isinstance(entity, Goal):
            self.stop()
        else:
            return

    def reset(self):
        self._position = self._initial_position


class Wall(Entity):
    def __init__(self, rect: Rect) -> None:
        position = Vector2(rect.topleft) + (Vector2(rect.width, rect.height) // 2)
        super().__init__(position, Vector2(rect.width, rect.height))


class Paddle(Entity):
    def __init__(self, position: Vector2) -> None:
        self._initial_position = position
        self._velocity = Vector2(0, 0)
        self._acceleration = Vector2(0, 0)
        super().__init__(position, Vector2(10, 80))

    def update(self, delta: float, environment):
        """Updates the padle each tick."""
        self._position = self._position + self._velocity * delta
        self._velocity = self._velocity + self._acceleration * delta

    def collide(self, delta, entity: Entity):
        if self._velocity.length_squared() == 0:
            while self.collision_rect.colliderect(entity.collision_rect):
                dir_center = (self._initial_position - self._position).normalize()
                self._position += dir_center
        else:
            while self.collision_rect.colliderect(entity.collision_rect):
                self._position -= self._velocity.normalize()
        if isinstance(entity, Wall):
            self._velocity.y = 0
            self._acceleration.y = 0
        else:
            return


class Goal(Entity):
    def __init__(self, rect: Rect) -> None:
        position = Vector2(rect.topleft) + (Vector2(rect.width, rect.height) // 2)
        super().__init__(position, Vector2(rect.width, rect.height))

    def collide(self, delta, entity):
        pass
