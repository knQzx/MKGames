import pygame


class LevelScreen:
    def start(self, setup):
        while True:
            setup.screen.fill(pygame.Color('yellow'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setup.operations.terminate()
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return setup.GameScreen()
            pygame.display.flip()
            setup.clock.tick(setup.FPS)
