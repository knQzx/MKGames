import pygame


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
            if not (sprite.rect.x + sprite.rect.w <= 0 or sprite.rect.x >= width or
                    sprite.rect.y + sprite.rect.h <= 0 or sprite.rect.y >= height):
                draw_group.add(sprite)
        draw_group.draw(screen)


class GameScreen:
    def start(self, setup):
        while True:
            setup.screen.fill(pygame.Color('green'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
            pygame.display.flip()
            setup.clock.tick(setup.FPS)
