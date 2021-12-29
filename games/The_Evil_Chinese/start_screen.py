import re
import time
from music_load import Music  # импорт музыки
import pygame


class LoadGame:
    def __init__(self):
        pass

    def walls_load(self, walls):
        return ([m.start() for m in re.finditer('q', walls.rstrip())])

    def floor_load(self, floor):
        return ([m.start() for m in re.finditer('_', floor.rstrip())])


class Rise:
    def __init__(self):
        pass

    def rise_load(self, rise):
        return ([m.start() for m in re.finditer('r', rise.rstrip())])


class Player:
    def __init__(self):
        pass

    def player_load(self, player):
        return ([m.start() for m in re.finditer('x', player.rstrip())])


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('The Evil Chinese v.1.0.0')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    # обещание великого правителя
    Music().rulers_promise('Обещание выдать миску риса.mp3')
    # музыка на фоне
    Music().background_music('Музыка на фон.mp3')
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        k = 0
        for el in open('data/levels/level_1/level_1').readlines():
            walls = LoadGame().walls_load(el)  # получаем список координат стен
            floar =  LoadGame().floor_load(el)  # получаем список координат пола
            playeer = Player().player_load(el)  # получаем список координат игрока
            rise = Rise().rise_load(el)  # получаем список координат риса
            if walls:  # --> если не пустой
                for el1 in walls:  # проходимся по элементам т.к. может быть не одна стена
                    el1 *= 10  # подгоняем под размеры
                    pygame.draw.line(screen, 'red', (el1, k), (el1, k + 20))
            if floar:  # --> если не пустой
                for el1 in floar:  # проходимся по элементам т.к. может быть не один пол
                    el1 *= 10  # подгоняем под размеры
                    pygame.draw.line(screen, 'red', (el1 - 10, k), (el1 + 10, k))
            if playeer:  # --> если не пустой
                # загружаем картинку нашего злобного китайца
                player = pygame.image.load('data/images/chinese.png').convert_alpha()
                player = pygame.transform.scale(player, (25, 25))
                screen.blit(player, (playeer[0] * 9.6, k - 6))
            if rise:  # --> если не пустой
                for el1 in rise:  # проходимся по элементам т.к. может быть не один рис
                    el1 *= 10  # подгоняем под размеры
                    pygame.draw.rect(screen, 'green', (el1, k, 5, 5))  # рисуем зеленый квадрат(рис)
            k += 20
            pygame.display.flip()
    pygame.quit()
