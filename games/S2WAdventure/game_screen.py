import pygame
import pytmx
import json
import operations


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2) - CELL_SIZE // 2
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2) - CELL_SIZE // 2

    def draw_group(self, group, screen):
        draw_group = pygame.sprite.Group()
        for sprite in group:
            if not (sprite.rect.x + sprite.rect.w <= 0 or sprite.rect.x >= screen.get_width() or
                    sprite.rect.y + sprite.rect.h <= 0 or sprite.rect.y >= screen.get_height()):
                draw_group.add(sprite)
        draw_group.draw(screen)


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pass


class GameScreen:
    def __init__(self, name):
        self.name = name

    def start(self, setup):
        self.setup = setup

        camera = Camera()
        self.tiles_group = pygame.sprite.Group()
        self.default_tiles_group = pygame.sprite.Group()
        self.death_tiles_group = pygame.sprite.Group()
        self.finish_tiles_group = pygame.sprite.Group()

        self.load_level()
        background = operations.load_image('forest.jpg')
        self.set_tiles(0)
        self.set_tiles(1)
        self.change_world_to(0)
        while True:
            setup.screen.fill(pygame.Color('green'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.change_world_to(0 if self.current_world == 1 else 1)
            operations.draw_background(self.setup.screen, background)
            camera.draw_group(self.tiles_group, self.setup.screen)
            pygame.display.flip()
            setup.clock.tick(setup.FPS)

    def load_level(self):
        with open(f'data/levels/{self.name}/level.json') as read_file:
            self.level = json.load(read_file)
        self.map = pytmx.load_pygame(f'data/levels/{self.name}/level.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.setup.height // 12
        self.default_tiles = [1, 2]
        self.death_tiles = [3, 4]
        self.finish_tile = 5

    def set_tiles(self, world):
        for y in range(self.height):
            for x in range(self.width):
                tile = pygame.sprite.Sprite()
                image = self.map.get_tile_image(x, y, world)
                if image is None:
                    continue
                tile.image = image.copy()
                tile.image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                tile.default_image = tile.image.copy()
                tile.rect = tile.image.get_rect()
                tile.rect.x, tile.rect.y = x * self.tile_size, y * self.tile_size
                tile.world = world
                tile_id = self.get_tile_id((x, y), world)
                if tile_id in self.default_tiles:
                    self.default_tiles_group.add(tile)
                if tile_id in self.death_tiles:
                    self.death_tiles_group.add(tile)
                if tile_id == self.finish_tile:
                    self.finish_tiles_group.add(tile)
                self.tiles_group.add(tile)

    def change_world_to(self, world_num):
        self.current_world = world_num
        for tile in self.tiles_group:
            if tile.world == world_num:
                tile.image = tile.default_image.copy()
            else:
                tile.image.set_alpha(75)

    def get_tile_id(self, position, layer):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, layer)]
