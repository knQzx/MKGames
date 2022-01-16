import pygame
import operations


class Lasers(pygame.sprite.Sprite):
    def __init__(self, x, y, game_screen):
        super().__init__()
        self.game_screen = game_screen
        self.image = pygame.transform.scale(operations.load_image('Lasers.png'), (self.game_screen.tile_size * 2.903,
                                                                                  self.game_screen.tile_size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = self.rect.x, self.rect.y

    def update(self):
        self.x -= (30 * self.game_screen.tile_size) / self.game_screen.setup.FPS
        self.rect.x = int(self.x)


class Rockets(pygame.sprite.Sprite):
    def __init__(self, x, y, game_screen):
        super().__init__()
        self.game_screen = game_screen
        self.image = pygame.transform.scale(operations.load_image('Rocket.png'), (self.game_screen.tile_size * 1.897,
                                                                                  self.game_screen.tile_size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = self.rect.x, self.rect.y

    def update(self):
        self.x -= (15 * self.game_screen.tile_size) / self.game_screen.setup.FPS
        self.rect.x = int(self.x)


class Hint(pygame.sprite.Sprite):
    def __init__(self, hero, game_screen, future_obj):
        super().__init__(game_screen.obstacles_group)
        self.future_obj = future_obj
        self.hero = hero
        self.game_screen = game_screen
        self.time = 0
        self.image = pygame.transform.scale(operations.load_image('Warning.png'), (self.game_screen.tile_size,
                                                                                   self.game_screen.tile_size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = self.game_screen.setup.width - self.rect.width, self.hero.rect.y

    def update(self):
        self.rect.y = self.hero.rect.y
        self.time += 1 / self.game_screen.setup.FPS
        if self.time >= 1:
            self.game_screen.obstacles_group.add(self.future_obj(self.rect.x, self.rect.y, self.game_screen))
            self.kill()
