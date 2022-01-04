import pygame
import operations
import json


class LevelScreen:
    def start(self, setup):
        self.setup = setup

        self.levels_group = pygame.sprite.Group()
        self.buttons_group = pygame.sprite.Group()
        self.cur_level_num = 0
        with open('data/levels/levels.json', 'r') as read_file:  # Import levels
            self.levels = json.load(read_file)
        self.add_levels()

        self.set_level_change_buttons()

        background = operations.load_image('Beer.png')
        while True:
            operations.draw_background(self.setup.screen, background)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.prev_button.rect.collidepoint(*event.pos):
                        self.cur_level_num -= 1
                        self.cur_level_num %= self.levels_count
                    if self.next_button.rect.collidepoint(*event.pos):
                        self.cur_level_num += 1
                        self.cur_level_num %= self.levels_count
                    for level_sprite in self.levels_group:
                        if level_sprite.num == self.cur_level_num:
                            if level_sprite.play_button.rect.collidepoint(*event.pos):
                                return self.setup.GameScreen(level_sprite.level)
            self.levels_group.update()
            self.levels_group.draw(self.setup.screen)
            self.buttons_group.update()
            self.buttons_group.draw(self.setup.screen)
            pygame.display.flip()
            setup.clock.tick(setup.FPS)

    def add_levels(self):
        self.levels_count = len(self.levels['level_names'])
        for num, level_name in enumerate(self.levels['level_names']):
            with open(f'data/levels/{level_name}/level.json') as read_file:
                level = json.load(read_file)
            level['name'] = level_name
            self.add_level(level, num)

    def add_level(self, level, num):
        level_sprite = LevelTitle(num, level, self)
        self.levels_group.add(level_sprite)

    def set_level_change_buttons(self):
        # prev button
        image = pygame.Surface((150, 150), pygame.SRCALPHA, 32)
        pygame.draw.polygon(
            image,
            pygame.Color('red'),
            (
                (0, image.get_height() // 2),
                (image.get_width(), 0),
                (image.get_width(), image.get_height())
            )
        )
        self.prev_button = Button(image, (0, self.setup.height // 2 - image.get_height() // 2))
        self.buttons_group.add(self.prev_button)

        # next button
        image = pygame.Surface((150, 150), pygame.SRCALPHA, 32)
        pygame.draw.polygon(
            image,
            pygame.Color('red'),
            (
                (0, 0),
                (image.get_width(), image.get_height() // 2),
                (0, image.get_height())
            )
        )
        self.next_button = Button(image, (self.setup.width - image.get_width(),
                                          self.setup.height // 2 - image.get_height() // 2))
        self.buttons_group.add(self.next_button)


class LevelTitle(pygame.sprite.Sprite):
    def __init__(self, num, level, level_screen: LevelScreen):
        super().__init__()
        self.num = num
        self.level = level
        self.name = level['name']
        self.stars = level['stars']
        self.completed = level['completed']
        self.level_screen = level_screen

        rel_size = 0.758, 0.723
        self.size = operations.get_screen_coords(self.level_screen.setup.screen, rel_size)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.draw()

    def update(self):
        self.rect.x, self.rect.y = self.level_screen.setup.width // 2 - self.rect.width // 2 + \
                                   self.level_screen.setup.width * (self.level_screen.cur_level_num - self.num), \
                                   operations.get_screen_coords(self.level_screen.setup.screen, (0, 0.161))[1]

    def draw(self):
        pygame.draw.rect(  # Draw shell
            self.image,
            pygame.Color("#E19006"),
            (0, 0, *self.size),
            0,
            50
        )

        font = pygame.font.Font(None, 96)  # Make font
        font.set_bold(True)

        if self.completed:  # Draw completed state
            text = font.render('Completed', True, pygame.Color('black'))
        else:
            text = font.render('Not completed', True, pygame.Color('black'))
        text_rect = text.get_rect()
        text_rect.x = self.size[0] // 2 - text.get_width() // 2
        text_rect.y = operations.get_screen_coords(self.image, (0, 0.022))[1]
        self.image.blit(
            text,
            text_rect
        )

        text = font.render(self.name, True, pygame.Color('black'))  # Draw level name
        text_rect = text.get_rect()
        text_rect.x = self.size[0] // 2 - text.get_width() // 2
        text_rect.y = operations.get_screen_coords(self.image, (0, 0.154))[1]
        self.image.blit(
            text,
            text_rect
        )

        indent = 30  # Draw stars
        count = self.stars
        star_image = pygame.transform.scale(operations.load_image('Star.png'), (145, 145))
        star_image_rect = star_image.get_rect()
        star_image_rect.x = self.size[0] // 2 - (star_image.get_width() * count + indent * (count - 1)) // 2
        star_image_rect.y = operations.get_screen_coords(self.image, (0, 0.30))[1]
        for _ in range(count):
            self.image.blit(
                star_image,
                star_image_rect
            )
            star_image_rect.x += star_image.get_width() + indent

        indent = 30
        play_button_text = font.render('Play', True, pygame.Color('black'))
        play_button_image = pygame.Surface(
            (indent * 2 + play_button_text.get_width(),
             indent * 2 + play_button_text.get_height()),
            pygame.SRCALPHA,
            32
        )
        pygame.draw.rect(
            play_button_image,
            pygame.Color('#EAC712'),
            play_button_image.get_rect()
        )
        play_button_text_rect = play_button_text.get_rect()
        play_button_text_rect.x, play_button_text_rect.y = indent, indent
        play_button_image.blit(
            play_button_text,
            play_button_text_rect
        )
        self.play_button = SpriteButton(self, play_button_image,
                                        (self.image.get_width() // 2 - play_button_text.get_width() // 2 - indent,
                                         operations.get_screen_coords(self.image, (0, 0.748))[1]))
        self.level_screen.buttons_group.add(self.play_button)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.pos = pos
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = pos


class SpriteButton(Button):
    def __init__(self, target, image, pos):
        super().__init__(image, pos)
        self.rect.x, self.rect.y = pos[0] + target.rect.x, pos[1] + target.rect.y
        self.target = target

    def update(self):
        self.rect.x, self.rect.y = self.pos[0] + self.target.rect.x, self.pos[1] + self.target.rect.y
