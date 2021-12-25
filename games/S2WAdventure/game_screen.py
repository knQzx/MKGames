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
            if not (sprite.rect.x + sprite.rect.w <= 0 or sprite.rect.x >= screen.width or
                    sprite.rect.y + sprite.rect.h <= 0 or sprite.rect.y >= screen.height):
                draw_group.add(sprite)
        draw_group.draw(screen)


class GameScreen:
    def __init__(self, name):
        self.name = name

    def start(self, setup):
        self.setup = setup

        camera = Camera()

        self.load_level()

        self.current_world = 0
        background = operations.load_image('forest.jpg')
        while True:
            setup.screen.fill(pygame.Color('green'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
            operations.draw_background(self.setup.screen, background)
            self.render(self.setup.screen, 0 if self.current_world == 1 else 1)
            self.render(self.setup.screen, self.current_world)
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

    def render(self, screen, layer):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, layer)
                if image is None:
                    continue
                image = image.copy()
                if layer != self.current_world:
                    image.set_alpha(50)
                image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position)]
