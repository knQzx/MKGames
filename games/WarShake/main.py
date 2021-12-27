import time
import pygame
import sys


class StartScreen:
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((680, 680))
        pygame.mixer.init()
        # загружаем фон и меняем название
        bg = pygame.image.load('data/images/background.png')
        pygame.display.set_caption('ДОКАЖИ ПАРТИИ СВОЮ СИЛУ ДУХА')
        # вставляем обещание великого правителя
        pygame.mixer.music.load("data/musics/Обещание выдать миску риса.mp3")
        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)
        # спим чтобы услышать обещание великого правителя
        time.sleep(9.5)
        # музыку про социальные кредиты ставим на фон
        pygame.mixer.music.load("data/musics/Музыка на фон.mp3")
        pygame.mixer.music.play(-1)

        while True:
            clock.tick(60)
            screen.blit(bg, (0,0))
            x,y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.update()


if __name__ == '__main__':
    StartScreen()
