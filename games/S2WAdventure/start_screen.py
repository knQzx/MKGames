import pygame
import json
import operations


class StartScreen:
    def start(self, setup):
        self.setup = setup
        pygame.mixer.music.stop()

        self.levels_group = pygame.sprite.Group()
        with open('data/levels/levels.json', 'r') as read_file:  # Import levels
            self.levels = json.load(read_file)
        self.add_levels()

        out = None
        while out is None:  # Working with UI
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for level in self.levels_group:
                        if level.rect.collidepoint(*event.pos):
                            out = setup.GameScreen(level.name)
                if event.type == pygame.MOUSEWHEEL:
                    move = event.x + event.y
                    if move > 0:
                        min_top = self.setup.size[1]
                        for level in self.levels_group:
                            min_top = min(min_top, level.rect.top)
                        if min_top < 0:
                            for level in self.levels_group:
                                level.rect = level.rect.move(0, move * 3)
                    if move < 0:
                        max_bottom = 0
                        for level in self.levels_group:
                            max_bottom = max(max_bottom, level.rect.bottom)
                        if max_bottom > self.setup.size[1]:
                            for level in self.levels_group:
                                level.rect = level.rect.move(0, move * 3)
            setup.screen.fill(pygame.Color('orange'))
            self.levels_group.draw(setup.screen)
            self.draw_title(self.setup.screen)
            self.draw_hint(self.setup.screen)

            self.setup.set_fps()
            setup.clock.tick()

            pygame.display.flip()
        return out

    def draw_hint(self, screen):
        text = ['Change world: "E"', 'Accelerate: "W"']
        x = 10
        y = 500
        for string in text:
            y += 60
            font = pygame.font.Font(None, 50)
            string = font.render(string, 1, pygame.Color('blue'))
            string_rect = string.get_rect()
            string_rect.x, string_rect.y = x, y
            screen.blit(string, string_rect)

    def draw_title(self, screen):
        image = operations.load_image('S2WAdventure title.png')
        rect = image.get_rect()
        rect.x, rect.y = 10, 10
        screen.blit(
            image,
            rect
        )

    def add_levels(self):
        for num, level_name in enumerate(self.levels['level_names']):
            with open(f'data/levels/{level_name}/level.json') as read_file:
                level = json.load(read_file)
            level['name'] = level_name
            self.add_level(level, num)

    def add_level(self, level, num):
        level_sprite = Level(self.setup.size, num, level['name'], level['score'])
        self.levels_group.add(level_sprite)


class Level(pygame.sprite.Sprite):
    def __init__(self, screen_size, num, name, score):
        super().__init__()

        self.size = 400, 100
        self.name, self.score = name, score
        self.indent = 10
        self.image = pygame.Surface(self.size)
        self.draw()
        self.rect = pygame.rect.Rect(
            screen_size[0] - self.size[0] - self.indent,
            (self.indent + self.size[1]) * num + self.indent,
            self.size[0],
            self.size[1]
        )

    def draw(self):
        pygame.draw.rect(
            self.image,
            pygame.Color('orange'),
            self.image.get_rect()
        )

        pygame.draw.rect(  # Draw shell
            self.image,
            pygame.Color('blue'),
            (0, 0, *self.size),
            2, 3
        )

        font = pygame.font.Font(None, 30)  # Draw level name
        string = font.render(self.name, 1, pygame.Color('blue'))
        level_name_rect = string.get_rect()
        level_name_rect.x, level_name_rect.y = self.size[0] // 2 - level_name_rect.width // 2, 10
        self.image.blit(string, level_name_rect)

        font = pygame.font.Font(None, 30)  # Draw score
        string = font.render(str(self.score) + '%', 1, pygame.Color('blue'))
        level_name_rect = string.get_rect()
        level_name_rect.x, level_name_rect.y = self.size[0] // 2 - level_name_rect.width // 2, self.size[1] // 2
        self.image.blit(string, level_name_rect)

        bar_size = (self.size[0] - 10), 10  # Draw background of progress bar
        pygame.draw.rect(
            self.image,
            pygame.Color('blue'),
            (self.size[0] // 2 - bar_size[0] // 2, self.size[1] - bar_size[1] * 2, *bar_size)
        )

        bar_size = (self.size[0] - 10) * self.score // 100, 10  # Draw progress bar
        pygame.draw.rect(
            self.image,
            pygame.Color('green'),
            (self.size[0] // 2 - bar_size[0] // 2, self.size[1] - bar_size[1] * 2, *bar_size)
        )
