import json

import pygame

import operations


class LevelScreen:  # Screen for select level
    def start(self, setup):  # Function launching window display
        self.setup = setup
        # The group will store the sprites of the level selection screens
        self.levels_group = pygame.sprite.Group()
        self.buttons_group = pygame.sprite.Group()  # The group will store the sprites of the buttons
        self.cur_level_num = 0  # Selected level select screen
        with open('data/levels/levels.json', 'r') as read_file:  # Import levels
            self.levels = json.load(read_file)
        self.add_levels()

        self.set_level_change_buttons()
        # load background image
        background = operations.load_image('Beer.png')
        while True:
            # draw background image
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
                                return self.setup.GameScreen(level_sprite.level['name'])
            # update our levels group
            self.levels_group.update()
            # draw setup.screen
            self.levels_group.draw(self.setup.screen)
            # update our buttons group
            self.buttons_group.update()
            # draw setup.screen
            self.buttons_group.draw(self.setup.screen)
            pygame.display.flip()
            setup.clock.tick(setup.FPS)

    def add_levels(self):  # --> function add level selection screen
        # here we count the levels
        self.levels_count = len(self.levels['level_names'])
        for num, level_name in enumerate(self.levels['level_names']):
            # open levels
            with open(f'data/levels/{level_name}/level.json') as read_file:
                # level to json format
                level = json.load(read_file)
            level['name'] = level_name
            # add level
            self.add_level(level, num)

    def add_level(self, level, num):  # --> function to add level
        level_sprite = LevelTitle(num, level, self)
        self.levels_group.add(level_sprite)

    def set_level_change_buttons(self):  # --> function to set level change buttons
        # prev button
        image = pygame.Surface((150, 150), pygame.SRCALPHA, 32)
        # draw
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
        # add to buttons group
        self.buttons_group.add(self.prev_button)

        # next button
        image = pygame.Surface((150, 150), pygame.SRCALPHA, 32)
        # draw
        pygame.draw.polygon(
            image,
            pygame.Color('red'),
            (
                (0, 0),
                (image.get_width(), image.get_height() // 2),
                (0, image.get_height())
            )
        )
        # initialization next button
        self.next_button = Button(image, (self.setup.width - image.get_width(),
                                          self.setup.height // 2 - image.get_height() // 2))
        # add next button to buttons group
        self.buttons_group.add(self.next_button)


class LevelTitle(pygame.sprite.Sprite):  # --> class of level select screen
    def __init__(self, num, level, level_screen: LevelScreen):  # --> setting default parameters
        super().__init__()
        self.num = num
        self.level = level
        self.name = level['name']
        self.stars = level['stars']
        self.completed = level['completed']
        self.level_screen = level_screen

        rel_size = 0.758, 0.723
        # set size
        self.size = operations.get_screen_coords(self.level_screen.setup.screen, rel_size)
        # set image
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        # set x and set y
        self.rect.x, self.rect.y = self.level_screen.setup.width // 2 - self.rect.width // 2 + \
                                   self.level_screen.setup.width * (
                                           self.num - self.level_screen.cur_level_num), \
                                   operations.get_screen_coords(self.level_screen.setup.screen,
                                                                (0, 0.161))[1]
        self.x, self.y = self.rect.x, self.rect.y
        # draw
        self.draw()

    def update(self):  # --> in this function we update the position
        move_x = self.level_screen.setup.width // 2 - self.rect.width // 2 + \
                 self.level_screen.setup.width * (self.num - self.level_screen.cur_level_num)

        if move_x - self.rect.x > 0:
            self.x += 4000 / self.level_screen.setup.FPS
            if self.level_screen.setup.width // 2 - self.rect.width // 2 + \
                    self.level_screen.setup.width * (
                    self.num - self.level_screen.cur_level_num) - self.x < 0:
                self.x = self.level_screen.setup.width // 2 - self.rect.width // 2 + \
                         self.level_screen.setup.width * (self.num - self.level_screen.cur_level_num)
        elif move_x - self.rect.x < 0:
            self.x -= 4000 / self.level_screen.setup.FPS
            if self.level_screen.setup.width // 2 - self.rect.width // 2 + \
                    self.level_screen.setup.width * (
                    self.num - self.level_screen.cur_level_num) - self.x > 0:
                self.x = self.level_screen.setup.width // 2 - self.rect.width // 2 + \
                         self.level_screen.setup.width * (self.num - self.level_screen.cur_level_num)
        self.rect.x = int(self.x)

    def draw(self):  # --> function to draw rect
        pygame.draw.rect(  # Draw shell
            self.image,
            pygame.Color("#E19006"),
            (0, 0, *self.size),
            0,
            50
        )
        # set font
        font = pygame.font.Font(None, 96)  # Make font
        # set bold
        font.set_bold(True)

        if self.completed:  # Draw completed state
            text = font.render('Completed', True, pygame.Color('black'))
        else:
            text = font.render('Not completed', True, pygame.Color('black'))
        text_rect = text.get_rect()
        # get x coordinate
        text_rect.x = self.size[0] // 2 - text.get_width() // 2
        # get y coordinate
        text_rect.y = operations.get_screen_coords(self.image, (0, 0.022))[1]
        self.image.blit(
            text,
            text_rect
        )
        # render font
        text = font.render(self.name, True, pygame.Color('black'))  # Draw level name
        text_rect = text.get_rect()
        # get x coordinate
        text_rect.x = self.size[0] // 2 - text.get_width() // 2
        # get y coordinate
        text_rect.y = operations.get_screen_coords(self.image, (0, 0.154))[1]
        self.image.blit(
            text,
            text_rect
        )

        indent = 30  # Draw stars
        count = self.stars
        # load star image
        star_image = pygame.transform.scale(operations.load_image('Star.png'), (145, 145))
        star_image_rect = star_image.get_rect()
        # set x coordinate
        star_image_rect.x = self.size[0] // 2 - (
                star_image.get_width() * count + indent * (count - 1)) // 2
        # get y coordinate
        star_image_rect.y = operations.get_screen_coords(self.image, (0, 0.30))[1]
        for _ in range(count):
            self.image.blit(
                star_image,
                star_image_rect
            )
            star_image_rect.x += star_image.get_width() + indent

        indent = 30  # Draw play button
        # initialization play button
        play_button_text = font.render('Play', True, pygame.Color('black'))
        play_button_image = pygame.Surface(
            (indent * 2 + play_button_text.get_width(),
             indent * 2 + play_button_text.get_height()),
            pygame.SRCALPHA,
            32
        )
        # draw button
        pygame.draw.rect(
            play_button_image,
            pygame.Color('#EAC712'),
            play_button_image.get_rect()
        )
        play_button_text_rect = play_button_text.get_rect()
        # get button x and y
        play_button_text_rect.x, play_button_text_rect.y = indent, indent
        play_button_image.blit(
            play_button_text,
            play_button_text_rect
        )
        # initialization button
        self.play_button = SpriteButton(self, play_button_image, (
            self.image.get_width() // 2 - play_button_text.get_width() // 2 - indent,
            operations.get_screen_coords(self.image, (0, 0.748))[1]))
        # add play button to level_screen.buttons_group
        self.level_screen.buttons_group.add(self.play_button)


class Button(pygame.sprite.Sprite):  # --> class for initializing buttons
    def __init__(self, image, pos):  # --> setting default parameters
        super().__init__()
        self.image = image
        self.pos = pos
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = pos


class SpriteButton(Button):  # --> class for initializing sprites
    def __init__(self, target, image, pos):  # --> setting default parameters
        super().__init__(image, pos)
        self.rect.x, self.rect.y = pos[0] + target.rect.x, pos[1] + target.rect.y
        self.target = target

    def update(self):  # --> function to set x and y
        self.rect.x, self.rect.y = self.pos[0] + self.target.rect.x, self.pos[1] + self.target.rect.y
