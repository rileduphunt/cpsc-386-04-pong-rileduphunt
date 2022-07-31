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
from ponggame.scene import TitleScene, GameScene
from ponggame import colors

class Game:
    """This is the game class"""
    def __init__(self, 
        argv, 
        window_width=800, 
        window_height=800, 
        window_title = "The bestest game ever!" ):
        """Initializer method for Game class"""
        print("Game is initializing")
        pygame.init()
        self._windowsize = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._windowsize)
        self._title = window_title
        pygame.display.set_caption(self._title)
        # self._game_is_over = False
        if not pygame.font:
            print("Warning: fonts are disabled.")
        if not pygame.mixer:
            print("Warning: sound is disabled.")
        
        self._scene_graph = None
    
    def build_scenegraph(self):
        self._scene_graph = [
            TitleScene(screen=self._screen, background_color=colors.RED, title="A title"),
            TitleScene(screen=self._screen, background_color=colors.RED, title="1"),
            TitleScene(screen=self._screen, background_color=colors.RED, title="2"),
            GameScene(screen=self._screen, background_color=colors.BLUE)
        ]
        

    def run(self):
        """Main game loop"""
        #while not self._game_is_over:
        for scene in self._scene_graph:
            while scene.is_valid:
                for event in pygame.event.get():
                    scene.handle_event(event)
                scene.update()
                scene.draw()
                # scene.process_tick()
                pygame.display.update()
                self._clock.tick(scene.framerate)
        print("You are out of scenes!")
        pygame.quit()
        return 0