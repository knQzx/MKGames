import json
import os

import pygame
import pytmx

import operations
import obstacles


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

        if not move_data['sprite_move']:
            self.game_screen.win = False
            self.game_screen.running = False

        self.game_screen.to_last_trigger_update -= move_data['d_coords'][0]

        self.dy += (5 * self.game_screen.ppm) / self.game_screen.setup.FPS


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
        self.triggers = [7, 8]
        self.death_tiles = [4, 9, 14, 11, 12, 13]
        self.end_tiles = [10, 15]

        pygame.mixer.music.load(f'data/music/{self.level["music"]}')
        pygame.mixer.music.play(-1)

    def set_tiles_and_triggers(self):  # Set tiles and triggers at field
        for y in range(self.height):
            for x in range(self.width):
                tile = pygame.sprite.Sprite()  # Set tiles
                image = self.map.get_tile_image(x, y, 0)
                if image is not None:
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
                image = self.map.get_tile_image(x, y, 1)
                if image is not None:
                    trigger.image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                    trigger.mask = pygame.mask.from_surface(trigger.image)
                    trigger.rect = trigger.image.get_rect()
                    trigger.rect.x, trigger.rect.y = x * self.tile_size, y * self.tile_size
                    trigger_id = self.get_tile_id((x, y), 1)
                    if trigger_id in self.triggers:
                        trigger.trigger_id = trigger_id
                        self.triggers_group.add(trigger)

    def get_tile_id(self, position, layer):  # Return id of tile at position
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, layer)]

    def check_lasers(self, hero):  # --> check collision with lasers
        for tile in self.death_tiles_group:
            if pygame.sprite.collide_mask(hero, tile):
                self.win = False
                self.running = False
                break

    def check_end(self, hero):
        for tile in self.end_tiles_group:
            if pygame.sprite.collide_mask(hero, tile):
                self.win = True
                self.running = False
                break

    def check_obstacles(self, hero):
        for obstacle in self.obstacles_group:
            if pygame.sprite.collide_mask(hero, obstacle):
                self.win = False
                self.running = False
                break

    def check_hit(self, hero, *collide_groups):
        prev_rect = hero.rect.copy()
        hero.rect.x += int(hero.dx)
        if operations.check_collide(hero, self.setup.screen, *collide_groups):
            changed_rect = hero.rect.copy()
            hit = True
            for sign in [-1, 1]:
                hero.rect.y += int((hero.dx + 5) * sign)
                if not operations.check_collide(hero, self.setup.screen, *collide_groups):
                    hit = False
                hero.rect = changed_rect.copy()
        else:
            hit = False
        hero.rect = prev_rect.copy()

        if hit:
            self.win = False
            self.running = False

    def check_stars(self, hero):
        for tile in self.stars_tiles_group:
            if pygame.sprite.collide_mask(hero, tile):
                self.stars += 1
                tile.kill()

    def check_triggers(self):
        for trigger in self.triggers_group:
            if pygame.sprite.collide_rect(self.hero, trigger):
                obstacles.Hint(self.hero, self, self.triggers_to_obstacle[trigger.trigger_id])
                self.to_last_trigger_update = self.tile_size * 2
                break

    def update_db(self):
        with open(os.path.join('data', 'levels', self.name, 'level.json'), 'r') as read_file:
            data = json.load(read_file)
        data['completed'] = data['completed'] or self.win
        if self.win:
            data['stars'] = max(data['stars'], self.stars)
        with open(os.path.join('data', 'levels', self.name, 'level.json'), 'w') as write_file:
            json.dump(data, write_file)

    def start(self, setup):
        self.setup = setup

        self.load_level()
        self.tile_size = self.setup.height // self.map.height
        self.ppm = self.tile_size / 2

        self.triggers_to_obstacle = {
            7: obstacles.Rockets,
            8: obstacles.Lasers
        }

        self.tiles_group = pygame.sprite.Group()
        self.default_tiles_group = pygame.sprite.Group()
        self.stars_tiles_group = pygame.sprite.Group()
        self.triggers_group = pygame.sprite.Group()
        self.death_tiles_group = pygame.sprite.Group()
        self.end_tiles_group = pygame.sprite.Group()
        self.set_tiles_and_triggers()

        camera = Camera()

        self.hero = Hero(0, self.map.height - 1, self)
        self.hero_group = pygame.sprite.Group()
        self.hero_group.add(self.hero)

        self.particles_group = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()
        self.to_last_trigger_update = 0

        background = operations.load_image(self.level['background'])
        space_clicked = pygame.key.get_pressed()[pygame.K_SPACE]

        self.win = None
        self.stars = 0
        self.running = True
        while True:
            if not self.running:
                pygame.mixer.music.pause()
                self.update_db()
                return self.setup.FinishScreen(self.name, self.win, self.stars)

            if self.to_last_trigger_update <= 0:
                self.check_triggers()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    operations.terminate()
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    if event.key == pygame.K_SPACE:
                        space_clicked = not space_clicked
            if space_clicked:
                self.hero.dy -= self.ppm * 8 / self.setup.FPS
                self.hero.sheet_state = 1
                self.particles_group.add(Particle(
                    pygame.transform.scale(operations.load_image('Smoke.png'),
                                           (self.tile_size * 0.2, self.tile_size * 0.2)),
                    self.hero.rect.x + self.tile_size * 0.4, self.hero.rect.y + self.tile_size * 0.4,
                    self
                ))
            self.hero.update()
            camera.update(self.hero, self)
            for tile in self.tiles_group:
                camera.apply(tile)
            for particle in self.particles_group:
                camera.apply(particle)
            for trigger in self.triggers_group:
                camera.apply(trigger)
            operations.draw_background(self.setup.screen, background)
            camera.draw_group(self.tiles_group, self.setup.screen)

            self.particles_group.update()
            self.particles_group.draw(self.setup.screen)

            self.obstacles_group.update()
            self.obstacles_group.draw(self.setup.screen)

            self.hero_group.draw(self.setup.screen)

            self.check_lasers(self.hero)  # Check collision with final game tiles
            self.check_end(self.hero)
            self.check_obstacles(self.hero)
            self.check_hit(self.hero, self.default_tiles_group)

            self.check_stars(self.hero)  # Check collision with non-final game tiles

            pygame.display.flip()
            setup.clock.tick(setup.FPS)

