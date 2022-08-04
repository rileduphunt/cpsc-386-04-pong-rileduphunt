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

from pygame.mixer import Sound
from ponggame import colors, data_dir
from typing import Dict, List, Protocol, Tuple, runtime_checkable
from pygame import Rect, Vector2, Surface, error, font, USEREVENT
from random import randrange
import pygame.gfxdraw
import pygame.draw
import pygame.time
import os


@runtime_checkable
class Collidable(Protocol):
    @property
    def collision_rect(self):
        pass

    @property
    def lines(self) -> List[Tuple[Vector2, Vector2]]:
        pass

    @property
    def normals(self) -> List[Vector2]:
        pass

    def collide(self, delta, entity):
        pass


class Entity:
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

    def __init__(
        self,
        position: Vector2,
        color: Tuple,
        radius=default_radius
    ) -> None:
        super().__init__(position, Vector2(2 * radius, 2 * radius))
        self._velocity = Vector2(0, 0)
        self.radius = radius
        self.color = color
        try:
            self.collision_sound = Sound(os.path.join(
                data_dir, "sounds", "collision.wav"
            ))
        except pygame.error as pygame_error:
            print(pygame_error)

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
            colors.BLACK
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
        elif isinstance(entity, Collidable):
            if self.collision_sound is not None:
                self.collision_sound.play()
            self._velocity = self.reflect(entity)
        super().collide(delta, entity)
        self._velocity *= 1.01

    def reflect(self, entity: Entity):
        """Reflect an entity off another entity."""
        # Step forward a unit so we're in contact with the entity.
        self._position += self._velocity.normalize()
        rect = self.collision_rect
        lines_normals = zip(entity.lines, entity.normals)
        relevant_normals: List[Vector2] = []
        # Step back now that we've got the points.
        self._position -= self._velocity.normalize()
        normal_sum = Vector2(0, 0)
        for line, normal in lines_normals:
            if rect.clipline(line):
                relevant_normals.append(line)
                normal_sum = normal_sum + normal
        return self._velocity.reflect(normal_sum)

    def start_timer(self):
        pygame.time.set_timer(
            USEREVENT + 1,
            millis=1000,
            loops=1
        )
        pygame.time.set_timer(
            USEREVENT + 2,
            millis=2000,
            loops=1
        )
        pygame.time.set_timer(
            USEREVENT + 3,
            millis=3000,
            loops=1
        )
        pygame.time.set_timer(
            USEREVENT + 4,
            millis=4000,
            loops=1
        )
        print("Start timer!")

    def make_color(self, color):
        """Returns a function that makes the object that color."""
        def func(event):
            print(color)
            self.color = color
        return func

    def reset(self):
        self._position = self._initial_position


class Wall(Entity):
    def __init__(self, rect: Rect) -> None:
        position = Vector2(rect.topleft) + (
            Vector2(rect.width, rect.height) // 2
        )
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
        if isinstance(entity, Wall):
            while self.collision_rect.colliderect(entity.collision_rect):
                dir_center = (
                    self._initial_position - self._position
                ).normalize()
                self._position += dir_center
            self.stop()
        super().collide(delta, entity)

    def move_up(self):
        self._acceleration.y = -1 / 60

    def move_down(self):
        self._acceleration.y = 1 / 60

    def stop(self):
        self._velocity *= 0
        self._acceleration *= 0
        pass


class AIPaddle(Paddle):
    def __init__(self, position: Vector2) -> None:
        super().__init__(position)
        self._cooldown = 0  # Number of milliseconds between direction changes

    def update(self, delta: float, environment: Dict[str, Entity]):
        self._cooldown = max(0, self._cooldown-delta)
        if self._cooldown == 0:
            self.decide(environment)
        super().update(delta, environment)

    def move_up(self):
        self._acceleration.y = -1 / 120

    def move_down(self):
        self._acceleration.y = 1 / 120

    def decide(self, environment):
        ball_pos: Vector2 = environment['ball']._position
        if (self._position.y > ball_pos.y and self._velocity.y == 0):
            self.move_up()
        elif (self._position.y < ball_pos.y and self._velocity.y == 0):
            self.move_down()
        elif (ball_pos - self._position).dot(self._velocity) <= 0:
            self.stop()
            pass

    def stop(self):
        # Cooldown of around the human reaction time.
        self._cooldown = randrange(150, 300)
        super().stop()


class Goal(Entity):
    def __init__(self, rect: Rect) -> None:
        position = Vector2(rect.topleft) + (
            Vector2(rect.width, rect.height) // 2
        )
        super().__init__(position, Vector2(rect.width, rect.height))


class TextDisplay(Entity):
    """Displays text on the screen, and updates when the text is changed."""
    def __init__(
        self,
        position: Vector2,
        font: font.Font,
        text: str,
    ) -> None:
        self.font = font
        self._text: str = text
        self._rendered = font.render(
            self._text,
            True,
            colors.BLACK
        )
        super().__init__(position, Vector2(0, 0))

    def draw(self, screen: Surface):
        screen.blit(
            self._rendered,
            self._position - Vector2(
                self._rendered.get_width() / 2,
                self._rendered.get_height() / 2
                ),
        )

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._rendered = self.font.render(
            self._text,
            True,
            colors.BLACK
        )
