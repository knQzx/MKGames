import pygame

import operations
from game_screen import GameScreen
from level_screen import LevelScreen


class Setup:
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        if display_info.current_w >= 2500:
            self.size = self.width, self.height = display_info.current_w - 1000, display_info.current_h - 80
        else:
            self.size = self.width, self.height = display_info.current_w, display_info.current_h
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.size = self.width, self.height = pygame.display.get_window_size()
        pygame.display.set_caption('BeerFlight')

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.operations = operations
        self.StartScreen = LevelScreen
        self.GameScreen = GameScreen

        self.state = self.StartScreen()
        while True:
            self.state = self.state.start(self)


if __name__ == '__main__':
    Setup()
