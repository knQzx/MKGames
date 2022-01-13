import json

import pygame
import pytmx

import operations


class Camera:  # Camera whose apply objects with main sprite
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target, game_screen):
        self.dx = -(target.rect.x + target.rect.w // 2 - game_screen.setup.width // 4)
        target.rect.x += self.dx
        target.x += self.dx

    def draw_group(self, group, screen):
        draw_group = pygame.sprite.Group()
        for sprite in group:
            if not (sprite.rect.x + sprite.rect.w <= 0 or sprite.rect.x >= screen.get_width() or
                    sprite.rect.y + sprite.rect.h <= 0 or sprite.rect.y >= screen.get_height()):
                draw_group.add(sprite)
        draw_group.draw(screen)


class Hero(pygame.sprite.Sprite):  # Sprite of main hero
    def __init__(self, x, y, game_screen):
        super().__init__()
        self.game_screen = game_screen
        self.ticks_to_change = 10
        self.sheet_state = 0
        self.cur_frame = 0
        self.sheets = [
            self.cut_sheet(operations.load_image('Walking_hero_sheet5x2.png'), 5, 2),
            self.cut_sheet(operations.load_image('Flying_hero_sheet1x1.png'), 1, 1)
        ]
        self.image = self.sheets[self.sheet_state][self.cur_frame]
        self.rect = pygame.Rect(0, 0, self.game_screen.tile_size * 0.9,
                                self.game_screen.tile_size * 0.9)
        self.rect = self.rect.move(x * game_screen.tile_size, y * game_screen.tile_size)
        self.mask = pygame.mask.from_surface(pygame.Surface((self.rect.width, self.rect.height)))
        self.mask.fill()
        self.x, self.y = self.rect.x, self.rect.y

        self.dx, self.dy = 5, 0

    def cut_sheet(self, sheet, columns, rows):
        frames = []
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)),
                    (self.game_screen.tile_size * 0.9, self.game_screen.tile_size * 0.9)))
        return frames

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(
            self.sheets[self.sheet_state] * self.ticks_to_change)
        self.image = self.sheets[self.sheet_state][self.cur_frame // self.ticks_to_change]

        move_data = operations.move_sprite(
            self,
            (self.dx * self.game_screen.tile_size / self.game_screen.setup.FPS, self.dy * 0.2),
            self.game_screen.setup.screen,
            self.game_screen.default_tiles_group
        )

        self.dy += (5 * self.game_screen.PPM) / self.game_screen.setup.FPS


class Particle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, game_screen):
        super().__init__(game_screen.particles_group)
        self.game_screen = game_screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.x, self.y = self.rect.x, self.rect.y
        self.width, self.height = self.image.get_size()

    def update(self):
        FPS = self.game_screen.setup.FPS
        self.width -= 20 / FPS
        self.height -= 20 / FPS
        self.rect.width, self.rect.height = int(self.width), int(self.height)
        self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))
        self.image.set_alpha(100 - (50 / FPS))
        if self.width < 0 or self.height < 0:
            self.kill()


class GameScreen:  # Screen for game at any level
    def __init__(self, name):
        self.name = name

    def load_level(self):  # Load selected level
        with open(f'data/levels/{self.name}/level.json') as read_file:
            self.level = json.load(read_file)
        self.map = pytmx.load_pygame(f'data/levels/{self.name}/level.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.default_tiles = [1, 2, 3]
        self.stars_tiles = [6]
        self.boss_triggers = [8]
        self.death_tiles = [4, 9, 14, 11, 12, 13]
        self.end_tiles = [9, 15]

        pygame.mixer.music.load(f'data/music/{self.level["music"]}')
        pygame.mixer.music.play(-1)

    def set_tiles_and_triggers(self):  # Set tiles and triggers at field
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
                    self.default_tiles_group.add(tile)
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
                    self.triggers_group.add(trigger)

    def get_tile_id(self, position, layer):  # Return id of tile at position
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, layer)]

    def check_lasers(self, hero):  # --> check collision with lasers
        for el in self.death_tiles_group:
            if pygame.sprite.collide_mask(hero, el):
                self.running = False
                break

    def start(self, setup):
        self.setup = setup

        self.load_level()
        self.tile_size = self.setup.height // self.map.height
        self.PPM = self.tile_size / 2

        self.tiles_group = pygame.sprite.Group()
        self.default_tiles_group = pygame.sprite.Group()
        self.stars_tiles_group = pygame.sprite.Group()
        self.triggers_group = pygame.sprite.Group()
        self.death_tiles_group = pygame.sprite.Group()
        self.end_tiles_group = pygame.sprite.Group()
        self.set_tiles_and_triggers()

        camera = Camera()

        hero = Hero(0, self.map.height - 1, self)
        hero_group = pygame.sprite.Group()
        hero_group.add(hero)

        self.particles_group = pygame.sprite.Group()

        background = operations.load_image(self.level['background'])
        space_clicked = pygame.key.get_pressed()[pygame.K_SPACE]
        self.running = True
        while True:
            operations.draw_background(self.setup.screen, background)
            if not self.running:
                pygame.mixer.music.pause()
                return self.setup.FinishScreen(self.name, False, 3)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    operations.terminate()
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    if event.key == pygame.K_SPACE:
                        space_clicked = not space_clicked
            if space_clicked:
                hero.dy -= self.PPM * 8 / self.setup.FPS
                hero.sheet_state = 1
                self.particles_group.add(Particle(
                    pygame.transform.scale(operations.load_image('Smoke.png'),
                                           (self.tile_size * 0.2, self.tile_size * 0.2)),
                    hero.rect.x + self.tile_size * 0.4, hero.rect.y + self.tile_size * 0.4,
                    self
                ))
            hero.update()
            camera.update(hero, self)
            for tile in self.tiles_group:
                camera.apply(tile)
            for particle in self.particles_group:
                camera.apply(particle)
            for trigger in self.triggers_group:
                camera.apply(trigger)
            camera.draw_group(self.tiles_group, self.setup.screen)

            self.particles_group.update()
            self.particles_group.draw(self.setup.screen)

            hero_group.draw(self.setup.screen)
            self.check_lasers(hero)
            pygame.display.flip()
            setup.clock.tick(setup.FPS)
