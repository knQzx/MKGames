import pygame
import json
import pytmx
import operations


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, game_screen):
        self.dx = -(target.rect.x + target.rect.w // 2 - game_screen.setup.width // 2)
        target.rect.x += self.dx
        target.x += self.dx

    def draw_group(self, group, screen):
        draw_group = pygame.sprite.Group()
        for sprite in group:
            if not (sprite.rect.x + sprite.rect.w <= 0 or sprite.rect.x >= screen.get_width() or
                    sprite.rect.y + sprite.rect.h <= 0 or sprite.rect.y >= screen.get_height()):
                draw_group.add(sprite)
        draw_group.draw(screen)


class GameScreen:
    def __init__(self, name):
        self.name = name

    def load_level(self):
        with open(f'data/levels/{self.name}/level.json') as read_file:
            self.level = json.load(read_file)
        self.map = pytmx.load_pygame(f'data/levels/{self.name}/level.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.default_tiles = [1, 2, 3, 6]
        self.stars_tiles = [5]
        self.boss_triggers = [7]
        self.death_tiles = [4, 8, 12, 9, 10, 11]
        self.end_tiles = [15, 16]

        pygame.mixer.music.load(f'data/music/{self.level["music"]}')
        pygame.mixer.music.play(-1)

    def set_tiles_and_triggers(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = pygame.sprite.Sprite()  # Set tiles
                image = self.map.get_tile_image(x, y, 0)
                if image is None:
                    continue
                tile.image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                tile.mask = pygame.mask.from_surface(tile.image)
                tile.rect = tile.image.get_rect()
                tile.rect.x, tile.rect.y = x * self.tile_size, y * self.tile_size
                tile_id = self.get_tile_id((x, y), 0)
                if tile_id in self.default_tiles:
                    self.death_tiles_group.add(tile)
                if tile_id in self.stars_tiles:
                    self.stars_tiles_group.add(tile)
                if tile_id in self.death_tiles:
                    self.death_tiles_group.add(tile)
                if tile_id in self.end_tiles:
                    self.end_tiles_group.add(tile)
                self.tiles_group.add(tile)

                trigger = pygame.sprite.Sprite()  # Set triggers
                image = self.map.get_tile_image(x, y, 0)
                if image is None:
                    continue
                trigger.image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                trigger.mask = pygame.mask.from_surface(tile.image)
                trigger.rect = tile.image.get_rect()
                trigger.rect.x, tile.rect.y = x * self.tile_size, y * self.tile_size
                trigger_id = self.get_tile_id((x, y), 0)
                if trigger_id in self.boss_triggers:
                    trigger.add(self.boss_triggers)

    def get_tile_id(self, position, layer):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, layer)]

    def start(self, setup):
        self.setup = setup

        self.load_level()
        self.tile_size = self.setup.height // self.map.height

        self.tiles_group = pygame.sprite.Group()
        self.default_tiles_group = pygame.sprite.Group()
        self.stars_tiles_group = pygame.sprite.Group()
        self.boss_triggers_group = pygame.sprite.Group()
        self.death_tiles_group = pygame.sprite.Group()
        self.end_tiles_group = pygame.sprite.Group()
        self.set_tiles_and_triggers()

        camera = Camera()

        background = operations.load_image(self.level['background'])
        while True:
            operations.draw_background(self.setup.screen, background)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
            camera.draw_group(self.tiles_group, self.setup.screen)
            pygame.display.flip()
            setup.clock.tick(setup.FPS)
