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
from types import FunctionType
from ponggame import colors
from typing import Dict, List, Protocol, Tuple
from pygame import Rect, Vector2, Surface
from random import randrange
import pygame.gfxdraw
import pygame.draw
import os


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
        """Draws the entity."""
        pygame.draw.rect(screen, colors.RED, self.collision_rect)

    def add_listener(self, event: str, listener: FunctionType):
        if event in self._listeners.keys():
            self._listeners[event].append(listener)
        else:
            self._listeners[event] = [listener]

    def _dispatch_listeners(self, event, *args):
        if event in self._listeners.keys():
            for listener in self._listeners[event]:
                listener(*args)

    @property
    def listeners(self):
        return self._listeners

    @property
    def collision_rect(self):
        return Rect(
            self._position - (self._dimensions / 2),
            self._dimensions
        )

    @property
    def normals(self) -> List[Vector2]:
        normals: List[Vector2] = []
        for line in self.lines:
            normals.append(
                (line[1]-line[0]).normalize().rotate(-90)
            )
        return normals

    @property
    def lines(self) -> List[Tuple[Vector2, Vector2]]:
        # List of lines defined by pairs of points
        lines = [
            (
                Vector2(self.collision_rect.topleft),
                Vector2(self.collision_rect.topright)
            ),
            (
                Vector2(self.collision_rect.topright),
                Vector2(self.collision_rect.bottomright)
            ),
            (
                Vector2(self.collision_rect.bottomright),
                Vector2(self.collision_rect.bottomleft)
            ),
            (
                Vector2(self.collision_rect.bottomleft),
                Vector2(self.collision_rect.topleft)
            ),
        ]
        return lines

    def collide(self, delta, entity):
        self._dispatch_listeners('collide', self, delta, entity)


class Ball(Entity):
    default_radius = 10

    def __init__(self, position: Vector2, color: Tuple, radius=default_radius) -> None:
        super().__init__(position, Vector2(2 * radius, 2 * radius))
        self._velocity = Vector2(0, 0)
        self.radius = radius
        self.color = color
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, 'assets/')
        self.soundeffect = os.path.join(data_dir)


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
        self._velocity = Vector2(25 / 60)
        self._velocity.rotate_ip(randrange(1, 90))
        self._velocity.rotate_ip(90 * randrange(4))
        # self._velocity = Vector2(0, -25/60)

    def stop(self):
        self._velocity = self._velocity * 0

    @property
    def is_moving(self):
        return self._velocity.length_squared() != 0.0

    def collide(self, delta, entity: Entity):
        if self._velocity.length_squared() != 0:
            while self.collision_rect.colliderect(entity.collision_rect):
                self._position -= self._velocity.normalize()
        if isinstance(entity, Goal):
            self.stop()
        elif isinstance(entity, Entity):
            self._velocity = self.reflect(entity)
        super().collide(delta, entity)
        # if isinstance(entity, Wall):
        #     self._velocity.y = -self._velocity.y
        # elif isinstance(entity, Paddle):
        #     #normal = self.get_collision_normal()
        #     self._velocity.x = -self._velocity.x
        # elif isinstance(entity, Goal):
        #     self.stop()
        # else:
        #     return

    def reflect(self, entity: Entity):
        """Reflect an entity off another entity."""
        # Step forward a unit so we're in contact with the entity.
        self._position += self._velocity.normalize()
        rect = self.collision_rect
        lines_normals = zip(entity.lines, entity.normals)
        relevant_normals: List[Vector2] = []
        # Step back now that we've got the points.
        self._position -= self._velocity.normalize()
        normal_sum = Vector2(0,0)
        for line, normal in lines_normals:
            if rect.clipline(line):
                relevant_normals.append(line)
                normal_sum = normal_sum + normal
        return self._velocity.reflect(normal_sum)

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
        super().__init__(position, Vector2(25, 80))

    def update(self, delta: float, environment):
        """Updates the padle each tick."""
        self._position = self._position + self._velocity * delta
        self._velocity = self._velocity + self._acceleration * delta

    def collide(self, delta, entity: Entity):
        #super().collide(delta, entity)
        if self._velocity.length_squared() == 0:
            while self.collision_rect.colliderect(entity.collision_rect):
                dir_center = (self._initial_position - self._position).normalize()
                self._position += dir_center
        if isinstance(entity, Wall):
            self._velocity.y = 0
            self._acceleration.y = 0
        else:
            return

    def stop(self):
        self._velocity *= 0
        self._acceleration *= 0


class Goal(Entity):
    def __init__(self, rect: Rect) -> None:
        position = Vector2(rect.topleft) + (Vector2(rect.width, rect.height) // 2)
        super().__init__(position, Vector2(rect.width, rect.height))

    # def collide(self, delta, entity):
    #     super().collide(delta, entity)
