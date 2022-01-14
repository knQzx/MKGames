import pygame

GREEN = (0, 250, 0)
BLACK = (0, 0, 0)
RED = (250, 0, 0)
WHITE = (255, 255, 255)


class Lasers_horizontally(pygame.sprite.Sprite):
    def __init__(self, x, y, game_screen):
        super().__init__()
        self.game_screen = game_screen
        self.speed = 5
        # uploading images
        self.image = pygame.image.load("data/images/Lasers.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = pygame.Rect(0, 0, self.game_screen.tile_size * 0.9,
                                self.game_screen.tile_size * 0.9)
        self.rect = self.rect.move(x * game_screen.tile_size, y * game_screen.tile_size)
        self.mask = pygame.mask.from_surface(pygame.Surface((self.rect.width, self.rect.height)))
        self.mask.fill()
        self.x, self.y = self.rect.x, self.rect.y

    def update(self):
        self.x += (6 * self.game_screen.PPM) / self.game_screen.setup.FPS
        self.rect.x = int(self.x)


class Rockets(pygame.sprite.Sprite):
    def __init__(self, x, y, game_screen):
        super().__init__()
        self.game_screen = game_screen
        self.speed = 5
        # uploading images
        self.image = pygame.image.load("data/images/Rocket.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = pygame.Rect(0, 0, self.game_screen.tile_size * 0.9,
                                self.game_screen.tile_size * 0.9)
        self.rect = self.rect.move(x * game_screen.tile_size, y * game_screen.tile_size)
        self.mask = pygame.mask.from_surface(pygame.Surface((self.rect.width, self.rect.height)))
        self.mask.fill()
        self.x, self.y = self.rect.x, self.rect.y

    def update(self):
        self.x += (6 * self.game_screen.PPM) / self.game_screen.setup.FPS
        self.rect.x = int(self.x)


class Hints(pygame.sprite.Sprite):
    def __init__(self, hero, game_screen, future_obj):
        super().__init__()
        self.future_obj = future_obj
        self.hero = hero
        self.game_screen = game_screen
        self.time = 0
        # Настройка картинки
        self.rect.x, self.rect.y = self.hero.rect.x, self.hero.rect.y

    def update(self):
        self.rect.x, self.rect.y = self.hero.rect.x, self.hero.rect.y
        self.time += 1 / self.game_screen.FPS
        if self.time >= 1:
            self.game_screen.obstacles_group.add(self.future_obj(self.rect.x, self.rect.y, self.game_screen))
