# Riley Hunt
# CPSC 386-01
# 2022-07-31
# hunt4riley@csu.fullerton.edu
# @rileduphunt
#
# Lab 04-00
#
# This is the __init__ file for the ponggame module.
#


"""This is the game!"""

import pygame
from ponggame.scene import Scene, TitleScene, GameScene
from ponggame import colors


class Game:
    """This is the game class"""

    def __init__(
        self,
        argv,
        window_title="Riley's Pong Game",
        window_width=800,
        window_height=800,
    ):
        """Initializer method for Game class"""
        print("Game is initializing")
        pygame.init()
        self._windowsize = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._windowsize)
        self._title = window_title
        self._args = argv
        pygame.display.set_caption(self._title)
        if not pygame.font:
            print("Warning: fonts are disabled.")
        if not pygame.mixer:
            print("Warning: sound is disabled.")

        self._game_is_over = False
        self._scene_graph = None
        self.scene = None

    def build_scenegraph(self):
        self._scene_graph = {
            'title': ['game'],
            'game': ['leaderboard', 'name_entry', 'game'],
            'name_entry': ['leaderboard'],
            'leaderboard': ['quit', 'title'],
        }
        scenes = {
            TitleScene(self._screen, colors.RED, title="A title"): 'title',
            GameScene(self._screen, colors.BLUE, soundtrack='sounds/interstellar-hero-02.wav'): 'game',
            TitleScene(
                self._screen, colors.RED, title="Name Entry"
            ): 'name_entry',
            TitleScene(
                self._screen, colors.RED, title="Leaderboard"
            ): 'leaderboard',
            None: 'quit',
        }
        self._scenes = {}
        for key in scenes:
            self._scenes[key] = scenes[key]
            self._scenes[scenes[key]] = key

    def next_scene(self, scene: Scene) -> Scene:
        """Returns the next scene"""
        print("Next scene")
        return self._scenes[
            self._scene_graph[self._scenes[scene]][scene.result]
        ]

    def run(self):
        """Main game loop"""
        scene = self._scenes['title']
        while not self._game_is_over:
            scene.start()
            while scene.is_valid:
                for event in pygame.event.get():
                    scene.handle_event(event)
                scene.update(self._clock.get_time())
                scene.draw()
                pygame.display.update()
                self._clock.tick(scene.framerate)
            scene.stop()
            scene = self.next_scene(scene)
            if scene is None:
                self._game_is_over = True

        print("You are out of scenes!")
        pygame.quit()
        return 0
