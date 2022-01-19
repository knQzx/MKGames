import pygame
import operations
from start_screen import StartScreen
from game_screen import GameScreen


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
        pygame.display.set_caption('S2WAdventure')

        self.clock = pygame.time.Clock()
        self.set_fps()

        self.operations = operations
        self.StartScreen = StartScreen
        self.GameScreen = GameScreen

        self.state = self.StartScreen()
        while True:
            self.state = self.state.start(self)

    def set_fps(self):
        self.FPS = self.clock.get_fps() if self.clock.get_fps() else 100000

        font = pygame.font.Font(None, 32)
        font.set_bold(True)
        fps_text = font.render(str(int(self.FPS)), True, pygame.color.Color('green'))
        self.screen.blit(fps_text, fps_text.get_rect())


if __name__ == '__main__':
    Setup()
