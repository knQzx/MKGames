import random
import sys
import time

import pygame


class StartScreen:
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((680, 680))
        pygame.mixer.init()
        # загружаем фон и меняем название
        background = 'background.png'
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
        # прописываем змейку
        size = 34
        half_size = size // 2
        res = 680
        res = res // size // 2 * 2 * size
        FPS = 12
        # прописываем рис
        all_sprites = pygame.sprite.Group()
        rise_image = pygame.image.load("data/images/rise.png")
        # указываем группу риса сразу
        rise = pygame.sprite.Sprite(all_sprites)
        rise.image = rise_image
        rise.rect = rise.image.get_rect()
        # задаём случайное местоположение рису
        rise.rect.x = random.randrange(500)
        rise.rect.y = random.randrange(500)
        while True:
            clock.tick(60)
            screen.blit(bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        # смена обоев
                        list_bg = ['background.png', 'background_2.png', 'background_3.png',
                                   'background_4.png']
                        list_bg.remove(background)
                        background = random.choice(list_bg)
                        bg = pygame.image.load(f'data/images/{background}')
                        screen.blit(bg, (0, 0))
                        pygame.display.flip()
                        pygame.display.update()
            all_sprites.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()


if __name__ == '__main__':
    StartScreen()
