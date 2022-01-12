import pygame


class FinishScreen:
    def __init__(self, level_name: str, win: bool, stars: int):
        self.level_name = level_name
        self.win = win
        self.stars = stars

    def draw(self):
        pass

    def start(self, setup):
        self.setup = setup

        self.image = pygame.Surface(self.setup.screen.get_size())
        self.draw()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
            self.setup.screen.blit(self.image, self.image.get_rect())
            pygame.display.flip()
            setup.clock.tick(setup.FPS)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.pos = pos
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = pos
