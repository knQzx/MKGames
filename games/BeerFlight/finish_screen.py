import pygame

import operations


class FinishScreen:
    def __init__(self, level_name: str, win: bool, stars: int):  # --> set default parameters
        self.level_name = level_name
        self.win = win
        self.stars = stars

    def draw(self):  # --> make function draw
        font = pygame.font.Font(None, 100)  # Draw win state
        font.set_bold(True)
        # check self.win, if true
        if self.win:
            text_str = 'Completed'
        # if false
        else:
            text_str = 'Lose'
        # render font parameters
        text = font.render(text_str, True, pygame.Color('yellow'))
        text_rect = text.get_rect()
        text_rect.x = self.image.get_width() // 2 - text.get_width() // 2
        # get screen coords
        text_rect.y = operations.get_screen_coords(self.image, (0, 0.25))[1]
        self.image.blit(text, text_rect)

        indent = 30  # Draw stars
        # make parameter count for the stars
        count = self.stars
        # load start image
        star_image = pygame.transform.scale(operations.load_image('Star.png'), (145, 145))
        star_image_rect = star_image.get_rect()
        # get x parameter
        star_image_rect.x = self.image.get_width() // 2 - (
                star_image.get_width() * count + indent * (count - 1)) // 2
        # get screen coords
        star_image_rect.y = operations.get_screen_coords(self.image, (0, 0.4))[1]
        for _ in range(count):
            self.image.blit(
                star_image,
                star_image_rect
            )
            star_image_rect.x += star_image.get_width() + indent

    def set_buttons(self):  # --> in this function, we directly make buttons
        # Place play again button
        play_again_image = pygame.transform.scale(operations.load_image('Play again.png'),
                                                  (100, 100))
        # get x parameter
        new_x = int(self.image.get_width() / 2 + play_again_image.get_rect().width / 2 * 1.5)
        # get y parameter
        new_y = self.image.get_height() // 2 + play_again_image.get_rect().height
        # initialization "play_again" buttons
        self.play_again_button = Button(
            play_again_image,
            (new_x, new_y)
        )
        # add buttons to group
        self.buttons_group.add(self.play_again_button)
        # initialization image for select level
        # Place select level button
        select_level_image = pygame.transform.scale(operations.load_image('Select level.png'),
                                                    (100, 100))
        # get x parameter
        new_x = int(self.image.get_width() / 2 - select_level_image.get_rect().width * 1.5)
        # get y parameter
        new_y = self.image.get_height() // 2 + select_level_image.get_rect().height
        # initialization "select_level" buttons
        self.select_level_button = Button(
            select_level_image,
            (new_x, new_y)
        )
        # add buttons to group
        self.buttons_group.add(self.select_level_button)

    def check_click(self, pos):  # --> in this function, we directly check the user's click
        if self.select_level_button.rect.collidepoint(*pos):
            self.screen_out = self.setup.LevelScreen()
        if self.play_again_button.rect.collidepoint(*pos):
            self.screen_out = self.setup.GameScreen(self.level_name)

    def set_music(self):  # --> in this function, we directly set win or lose musics
        if self.win:
            pygame.mixer.music.load(f'data/music/Win.mp3')
        else:
            pygame.mixer.music.load(f'data/music/Lose.mp3')
        pygame.mixer.music.play(1)

    def start(self, setup):  # --> this is our start function
        self.setup = setup
        # set music
        self.set_music()

        self.image = pygame.Surface(self.setup.screen.get_size(), pygame.SRCALPHA, 32)
        self.draw()
        # initialization buttons group
        self.buttons_group = pygame.sprite.Group()
        self.set_buttons()
        # set default screen_out parameter as None
        self.screen_out = None
        while True:
            # screen fill to blue
            self.setup.screen.fill(pygame.Color('blue'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos)
            # check screen_out
            if self.screen_out is not None:
                pygame.mixer.music.pause()
                return self.screen_out
            self.setup.screen.blit(self.image, self.image.get_rect())
            self.buttons_group.draw(self.setup.screen)
            pygame.display.flip()
            setup.clock.tick(setup.FPS)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos):  # --> set default parameters
        super().__init__()
        self.image = image
        self.pos = pos
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = pos
