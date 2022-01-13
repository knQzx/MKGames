import pygame
from game_screen import GameScreen
from level_screen import LevelScreen
from finish_screen import FinishScreen


class Setup:  # Screen loop and program data
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()  # Window settings
        if display_info.current_w >= 2500:
            self.size = self.width, self.height = display_info.current_w - 1000, display_info.current_h - 80
        else:
            self.size = self.width, self.height = display_info.current_w, display_info.current_h
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.size = self.width, self.height = pygame.display.get_window_size()
        pygame.display.set_caption('BeerFlight')

        self.clock = pygame.time.Clock()  # Time settings
        self.FPS = 60

        self.LevelScreen = LevelScreen  # Screen storage
        self.GameScreen = GameScreen
        self.FinishScreen = FinishScreen

        self.state = self.LevelScreen()  # Screen loop
        while True:
            self.state = self.state.start(self)


if __name__ == '__main__':
    Setup()  # Start of program
