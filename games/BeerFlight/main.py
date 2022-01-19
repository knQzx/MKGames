import pygame

from finish_screen import FinishScreen
from game_screen import GameScreen
from level_screen import LevelScreen
import operations


class Setup:  # --> screen loop and program data
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()  # Window settings
        if display_info.current_w >= 2500:
            self.width, self.height = display_info.current_w - 1000, display_info.current_h - 80
            self.size = self.width, self.height
        else:
            self.size = self.width, self.height = display_info.current_w, display_info.current_h
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.size = self.width, self.height = pygame.display.get_window_size()
        pygame.display.set_caption('BeerFlight')

        self.clock = pygame.time.Clock()  # Time settings
        self.set_fps()

        self.LevelScreen = LevelScreen  # Screen storage
        self.GameScreen = GameScreen
        self.FinishScreen = FinishScreen

        self.state = self.LevelScreen()  # Screen loop
        while self.state is not None:
            self.state = self.state.start(self)
        operations.terminate()

    def set_fps(self):
        self.FPS = self.clock.get_fps() if self.clock.get_fps() else 100000

        font = pygame.font.Font(None, 32)
        font.set_bold(True)
        fps_text = font.render(str(int(self.FPS)), True, pygame.color.Color('green'))
        self.screen.blit(fps_text, fps_text.get_rect())


if __name__ == '__main__':
    Setup()  # Start of program
