import pygame
import operations


class FinishScreen:
    def __init__(self, level_name: str, win: bool, stars: int):
        self.level_name = level_name
        self.win = win
        self.stars = stars

    def draw(self):
        font = pygame.font.Font(None, 100)  # Draw win state
        font.set_bold(True)
        if self.win:
            text_str = 'Completed'
        else:
            text_str = 'Lose'
        text = font.render(text_str, True, pygame.Color('yellow'))
        text_rect = text.get_rect()
        text_rect.x = self.image.get_width() // 2 - text.get_width() // 2
        text_rect.y = operations.get_screen_coords(self.image, (0, 0.25))[1]
        self.image.blit(text, text_rect)

        if self.win:  # Draw stars
            indent = 30
            count = self.stars
            star_image = pygame.transform.scale(operations.load_image('Star.png'), (145, 145))
            star_image_rect = star_image.get_rect()
            star_image_rect.x = self.image.get_width() // 2 - (
                    star_image.get_width() * count + indent * (count - 1)) // 2
            star_image_rect.y = operations.get_screen_coords(self.image, (0, 0.4))[1]
            for _ in range(count):
                self.image.blit(
                    star_image,
                    star_image_rect
                )
                star_image_rect.x += star_image.get_width() + indent

    def set_buttons(self):
        play_again_image = pygame.transform.scale(operations.load_image('Play again.png'), (100, 100))  # Place play again button
        new_x = int(self.image.get_width() / 2 + play_again_image.get_rect().width / 2 * 1.5)
        new_y = self.image.get_height() // 2 + play_again_image.get_rect().height
        self.play_again_button = Button(
            play_again_image,
            (new_x, new_y)
        )
        self.buttons_group.add(self.play_again_button)

        select_level_image = pygame.transform.scale(operations.load_image('Select level.png'), (100, 100))  # Place select level button
        new_x = int(self.image.get_width() / 2 - select_level_image.get_rect().width * 1.5)
        new_y = self.image.get_height() // 2 + select_level_image.get_rect().height
        self.select_level_button = Button(
            select_level_image,
            (new_x, new_y)
        )
        self.buttons_group.add(self.select_level_button)

    def check_click(self, pos):
        if self.select_level_button.rect.collidepoint(*pos):
            self.screen_out = self.setup.LevelScreen()
        if self.play_again_button.rect.collidepoint(*pos):
            self.screen_out = self.setup.GameScreen(self.level_name)

    def set_music(self):
        if self.win:
            pygame.mixer.music.load(f'data/music/Win.mp3')
        else:
            pygame.mixer.music.load(f'data/music/Lose.mp3')
        pygame.mixer.music.play(1)

    def start(self, setup):
        self.setup = setup

        self.set_music()

        self.image = pygame.Surface(self.setup.screen.get_size(), pygame.SRCALPHA, 32)
        self.draw()

        self.buttons_group = pygame.sprite.Group()
        self.set_buttons()

        self.screen_out = None
        while True:
            self.setup.screen.fill(pygame.Color('blue'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    operations.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos)
            if self.screen_out is not None:
                pygame.mixer.music.pause()
                return self.screen_out
            self.setup.screen.blit(self.image, self.image.get_rect())
            self.buttons_group.draw(self.setup.screen)
            pygame.display.flip()
            setup.clock.tick(setup.FPS)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.pos = pos
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = pos
