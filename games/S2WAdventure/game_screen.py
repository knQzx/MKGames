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
        self.cut_sheet(operations.load_image('hero.png'), 2, 2)

        self.current_speed = 0
        self.speeds = [3 * self.game_screen.tile_size, 4 * self.game_screen.tile_size]
        self.speed = self.speeds[self.current_speed]

        self.dx, self.dy = self.speed, 0
        self.air_time = 0
        self.fix_up_count = 0
        self.distance_from_last_block = 0

        self.image = self.frames[self.game_screen.current_world][self.current_speed]
        self.image = pygame.transform.scale(self.image, (self.game_screen.tile_size, self.game_screen.tile_size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x * game_screen.tile_size,
                                   y * game_screen.tile_size + self.game_screen.tile_size // 2)
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
        prev_rect = self.rect.copy()

        self.dy += 30 * self.speed * self.air_time ** 2 / 9.8
        self.dx = self.speed
        self.x += self.dx / self.game_screen.setup.FPS
        self.distance_from_last_block += self.dx / self.game_screen.setup.FPS
        if self.distance_from_last_block // self.game_screen.tile_size != 0:
            self.fix_up_count = 0
            self.distance_from_last_block = 0
        self.y += self.dy / self.game_screen.setup.FPS
        self.dy -= 30 * self.speed * self.air_time ** 2 / 9.8
        self.air_time += 1 / self.game_screen.setup.FPS

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        for tile in self.game_screen.tiles_group:
            if tile.world == self.game_screen.current_world and pygame.sprite.collide_mask(self, tile):
                if tile in self.game_screen.death_tiles_group:
                    self.game_screen.finish_game(False)
                if tile in self.game_screen.finish_tiles_group:
                    self.game_screen.finish_game(True)
                self.dy = 0
                self.dx = 0
                self.air_time = 0
                cur_rect = self.rect.copy()

                test_rect = prev_rect
                test_rect.y = self.rect.y
                self.rect = test_rect.copy()
                if pygame.sprite.collide_mask(self, tile):
                    self.y = prev_rect.y
                    self.rect.y = int(self.y)
                self.rect = cur_rect.copy()

                test_rect = prev_rect
                test_rect.x = self.rect.x
                test_rect.y -= self.game_screen.tile_size // 4
                self.rect = test_rect.copy()
                if pygame.sprite.collide_mask(self, tile):
                    self.x = prev_rect.x
                    self.game_screen.finish_game(False)
                self.rect = cur_rect.copy()

                while pygame.sprite.collide_mask(self, tile) and self.fix_up_count <= self.game_screen.tile_size // 4:
                    self.rect.y -= 1
                    self.y -= 1
                    self.fix_up_count += 1

        if self.rect.bottom < 0 or self.rect.top > self.game_screen.setup.height or \
                self.rect.left < 0 or self.rect.right > self.game_screen.setup.width:
            self.game_screen.finish_game(False)


class GameScreen:
    def __init__(self, name):
        self.name = name

    def start(self, setup):
        self.setup = setup
        self.load_level()
        self.tile_size = self.setup.height // 12

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

        background = operations.load_image('forest.jpg')
        self.running = True
        while True:
            space_clicked = False
            for event in pygame.event.get():
                if not self.running:
                    return self.setup.StartScreen()
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
                        self.hero.rect.y += 1
                        self.hero.y += 1
                        for tile in self.tiles_group:
                            if tile.world == self.current_world and pygame.sprite.collide_mask(self.hero, tile):
                                self.hero.dy -= 6.5 * self.tile_size
                                break
                        self.hero.rect.y += 1
                        self.hero.y += 1
                        space_clicked = True
                    if event.key == pygame.K_w and self.running:
                        self.hero.change_speed()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w and self.running:
                        self.hero.change_speed()
            if self.running:
                self.hero.update()
                camera.update(self.hero, self)

                for tile in self.tiles_group:
                    camera.apply(tile)

            operations.draw_background(self.setup.screen, background)
            camera.draw_group(self.tiles_group, self.setup.screen)
            self.hero_group.draw(self.setup.screen)
            pygame.display.flip()
            setup.clock.tick(self.setup.FPS)

    def load_level(self):
        with open(f'data/levels/{self.name}/level.json') as read_file:
            self.level = json.load(read_file)
        self.map = pytmx.load_pygame(f'data/levels/{self.name}/level.tmx')
        self.height = self.map.height
        self.width = self.map.width
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

    def finish_game(self, win):
        print(win)
        self.running = False
