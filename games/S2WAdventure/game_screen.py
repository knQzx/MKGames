import os
import sqlite3

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


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, game_screen):
        super().__init__(game_screen.hero_group)
        self.game_screen = game_screen

        self.frames = []
        self.cut_sheet(operations.load_image('Hero.png'), 2, 2)

        self.current_speed = 0 if not pygame.key.get_pressed()[pygame.K_w] else 1
        self.speeds = [3, 4]
        self.speed = self.speeds[self.current_speed]

        self.dx, self.dy = self.speed, 0
        self.distance = 0

        self.image = self.frames[self.game_screen.current_world][self.current_speed]
        self.image = pygame.transform.scale(self.image, (self.game_screen.tile_size, self.game_screen.tile_size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x * game_screen.tile_size,
                                   y * game_screen.tile_size)
        self.x, self.y = self.rect.x, self.rect.y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            self.frames.append([])
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames[-1].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def change_speed(self):
        self.current_speed = (self.current_speed + 1) % len(self.speeds)
        self.image = self.frames[self.game_screen.current_world][self.current_speed]
        self.image = pygame.transform.scale(self.image, (self.game_screen.tile_size, self.game_screen.tile_size))
        self.speed = self.speeds[self.current_speed]

    def update(self):
        move_data = operations.move_sprite(self, (self.dx * self.game_screen.tile_size / self.game_screen.setup.FPS,
                                                  self.dy / self.game_screen.setup.FPS), self.game_screen.current_world,
                                           self.game_screen.default_tiles_group)

        self.distance += move_data['d_coords'][0]

        self.dx = self.speed
        self.dy += (self.game_screen.G * self.game_screen.ppm) / self.game_screen.setup.FPS

        if self.rect.bottom < 0 or self.rect.top > self.game_screen.setup.height or \
                self.rect.left < 0 or self.rect.right > self.game_screen.setup.width:
            self.game_screen.finish_game()


class FinishTitle(pygame.sprite.Sprite):
    def __init__(self, game_screen):
        super().__init__(game_screen.finish_title_group)
        self.game_screen = game_screen
        self.score = int(self.game_screen.hero.distance / self.game_screen.tile_size / self.game_screen.width * 100)

        self.image = pygame.Surface(self.game_screen.setup.size, pygame.SRCALPHA, 32)
        self.size = self.game_screen.setup.size
        self.draw()
        self.rect = self.image.get_rect()

        self.rect.x = -self.game_screen.setup.width
        self.x = self.rect.x

    def draw(self):
        pygame.draw.rect(  # Draw shell
            self.image,
            pygame.Color('blue'),
            (0, 0, *self.size),
            10, 10
        )

        font = pygame.font.Font(None, 30)  # Draw score
        string = font.render(str(self.score) + '%', 1, pygame.Color('blue'))
        level_name_rect = string.get_rect()
        level_name_rect.x, level_name_rect.y = self.size[0] // 2 - level_name_rect.width // 2, self.size[1] // 2
        self.image.blit(string, level_name_rect)

        bar_size = (self.size[0] - 40), 10  # Draw background of progress bar
        pygame.draw.rect(
            self.image,
            pygame.Color('blue'),
            (self.size[0] // 2 - bar_size[0] // 2, self.size[1] // 2 + bar_size[1] * 2, *bar_size)
        )

        bar_size = (self.size[0] - 40) * self.score // 100, 10  # Draw progress bar
        pygame.draw.rect(
            self.image,
            pygame.Color('green'),
            (self.size[0] // 2 - bar_size[0] // 2, self.size[1] // 2 + bar_size[1] * 2, *bar_size)
        )

        play_again_image = pygame.transform.scale(operations.load_image('Play again.png'),
                                                  (100, 100))  # Place play again button
        new_x = int(self.size[0] / 2 + play_again_image.get_rect().width / 2 * 1.5)
        new_y = self.size[1] // 2 + play_again_image.get_rect().height
        self.play_again_button = Button(
            play_again_image,
            self,
            (new_x, new_y),
            self.game_screen.finish_title_group
        )

        select_level_image = pygame.transform.scale(operations.load_image('Select level.png'),
                                                    (100, 100))  # Place select level button
        new_x = int(self.size[0] / 2 - select_level_image.get_rect().width * 1.5)
        new_y = self.size[1] // 2 + select_level_image.get_rect().height
        self.select_level_button = Button(
            select_level_image,
            self,
            (new_x, new_y),
            self.game_screen.finish_title_group
        )

    def check_click(self, pos):
        if self.select_level_button.rect.collidepoint(*pos):
            self.game_screen.out = self.game_screen.setup.StartScreen()
        if self.play_again_button.rect.collidepoint(*pos):
            self.game_screen.out = self.game_screen.setup.GameScreen(self.game_screen.name)

    def update(self):
        if self.x < 0:
            self.x += 2000 / self.game_screen.setup.FPS
            self.rect.x = min(0, int(self.x))


class Button(pygame.sprite.Sprite):
    def __init__(self, image, target, target_pos, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.target = target
        self.target_pos = target_pos

    def update(self):
        self.rect.x, self.rect.y = self.target.rect.x + self.target_pos[0], self.target.rect.y + self.target_pos[1]


class GameScreen:
    def __init__(self, name):
        self.name = name

    def start(self, setup):
        self.setup = setup
        self.load_level()
        self.tile_size = self.setup.height // 12
        self.ppm = self.tile_size * 1.8
        self.G = 9.8
        self.JUMP_STRENGTH = 6

        self.tiles_group = pygame.sprite.Group()
        self.default_tiles_group = pygame.sprite.Group()
        self.death_tiles_group = pygame.sprite.Group()
        self.finish_tiles_group = pygame.sprite.Group()
        self.set_tiles(0)
        self.set_tiles(1)
        self.change_world_to(0)

        camera = Camera()
        self.hero_group = pygame.sprite.Group()
        self.hero = Hero(0, self.height - 2, self)

        background = operations.load_image(self.level['background'])
        self.running = True
        win_check = False
        while True:
            # make +1 money if you win
            if float(self.hero.distance / self.tile_size / self.width * 100) >= 100 and not win_check:
                start_dir_path = os.getcwd()
                os.chdir('../..')
                conn = sqlite3.connect("database.sqlite")
                cursor = conn.cursor()
                coins = cursor.execute("""SELECT Coins FROM User""").fetchone()
                coins_now = int(coins[0])
                coins_will = str(coins_now + 1)
                sql_link = f"""UPDATE User SET Coins={coins_will}"""
                cursor.execute(sql_link)
                conn.commit()
                os.chdir(start_dir_path)
                win_check = True

            if not self.running:
                if self.out is not None:
                    return self.out

            space_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and self.running:
                        collide = False
                        for tile in self.tiles_group:
                            if tile.world != self.current_world and pygame.sprite.collide_mask(self.hero, tile):
                                collide = True
                        if not collide:
                            self.change_world_to(0 if self.current_world == 1 else 1)
                            self.hero.image = self.hero.frames[self.current_world][self.hero.current_speed]
                            self.hero.image = pygame.transform.scale(self.hero.image, (self.tile_size, self.tile_size))
                    if event.key == pygame.K_SPACE and self.running:
                        if space_clicked:
                            continue
                        self.hero.rect.y += self.tile_size // 2
                        for tile in self.tiles_group:
                            if tile.world == self.current_world and pygame.sprite.collide_mask(self.hero, tile):
                                self.hero.dy -= self.ppm * self.JUMP_STRENGTH
                                break
                        self.hero.rect.y -= self.tile_size // 2
                        space_clicked = True
                    if event.key == pygame.K_w and self.running:
                        self.hero.change_speed()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w and self.running:
                        self.hero.change_speed()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.running:
                        self.finish_title.check_click(event.pos)
            if self.running:
                self.hero.update()
                camera.update(self.hero, self)
                for tile in self.tiles_group:
                    camera.apply(tile)

            operations.draw_background(self.setup.screen, background)
            camera.draw_group(self.tiles_group, self.setup.screen)
            self.hero_group.draw(self.setup.screen)
            if not self.running:
                self.finish_title_group.update()
                self.finish_title_group.draw(self.setup.screen)

            for tile in self.death_tiles_group:
                if pygame.sprite.collide_mask(self.hero, tile) and tile.world == self.current_world:
                    self.finish_game()

            self.hero.rect.x += self.tile_size // 8
            self.hero.rect.y -= 1
            for tile in self.default_tiles_group:
                if pygame.sprite.collide_mask(self.hero, tile) and tile.world == self.current_world:
                    self.finish_game()
            self.hero.rect.x -= self.tile_size // 8
            self.hero.rect.y += 1

            for tile in self.finish_tiles_group:
                if pygame.sprite.collide_mask(self.hero, tile):
                    self.hero.distance = self.tile_size * self.width
                    self.finish_game()

            self.setup.set_fps()
            setup.clock.tick()

            pygame.display.flip()

    def load_level(self):
        with open(f'data/levels/{self.name}/level.json') as read_file:
            self.level = json.load(read_file)
        self.map = pytmx.load_pygame(f'data/levels/{self.name}/level.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.default_tiles = [1, 2]
        self.death_tiles = [3, 4]
        self.finish_tile = 5

        pygame.mixer.music.load(f'data/music/{self.level["music"]}')
        pygame.mixer.music.play(-1)

    def set_tiles(self, world):
        for y in range(self.height):
            for x in range(self.width):
                tile = pygame.sprite.Sprite()
                image = self.map.get_tile_image(x, y, world)
                if image is None:
                    continue
                tile.image = image.copy()
                tile.image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                tile.mask = pygame.mask.from_surface(tile.image)
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

    def finish_game(self):
        if not self.running:
            return
        self.running = False
        self.out = None
        self.finish_title_group = pygame.sprite.Group()
        self.finish_title = FinishTitle(self)

        with open(f'data/levels/{self.name}/level.json') as read_file:
            level_data = json.load(read_file)
        level_data['score'] = max(level_data['score'], int(self.hero.distance / self.tile_size / self.width * 100))
        with open(f'data/levels/{self.name}/level.json', 'w') as write_file:
            json.dump(level_data, write_file)
