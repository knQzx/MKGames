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
    pygame.font.init()
    pygame.display.set_caption('The Evil Chinese v.1.0.0')
    size = width, height = 800, 800
    sxr = 30
    screen = pygame.display.set_mode(size)
    # обещание великого правителя
    Music().rulers_promise('Обещание выдать миску риса.mp3')
    # музыка на фоне
    Music().background_music('Музыка на фон.mp3')
    #
    k = 0
    rise_x_y = {}
    for el in open('data/levels/level_1/level_1').readlines():
        playeer = Player().player_load(el)  # получаем список координат игрока
        walls = LoadGame().walls_load(el)  # получаем список координат стен
        floar = LoadGame().floor_load(el)  # получаем список координат пола
        rise = Rise().rise_load(el)  # получаем список координат риса
        if rise:
            new_rise = [el1 * 10 for el1 in rise]
            rise_x_y[k] = new_rise
        if playeer:  # --> если не пустой
            # загружаем картинку нашего злобного китайца
            player = pygame.image.load('data/images/chinese.png').convert_alpha()
            player = pygame.transform.scale(player, (25, 25))
            x_pos = playeer[0] * 9.6
            y_pos = k - 6
        k += 20
    #
    running = True
    clock = pygame.time.Clock()
    v = 25  # пикселей в секунду
    # наш счет
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('Количество риса: 0', False, 'blue')
    screen.blit(textsurface, (0, 0))
    rise_result = 0
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        k = 0
        screen.fill((0, 0, 0))
        textsurface = myfont.render(f'Количество риса: {rise_result}', False, 'blue')
        screen.blit(textsurface, (600, 0))
        for el in open('data/levels/level_1/level_1').readlines():
            walls = LoadGame().walls_load(el)  # получаем список координат стен
            floar = LoadGame().floor_load(el)  # получаем список координат пола
            rise = Rise().rise_load(el)  # получаем список координат риса
            if walls:  # --> если не пустой
                for el1 in walls:  # проходимся по элементам т.к. может быть не одна стена
                    el1 *= 10  # подгоняем под размеры
                    pygame.draw.line(screen, 'red', (el1, k), (el1, k + 20))
            if floar:  # --> если не пустой
                for el1 in floar:  # проходимся по элементам т.к. может быть не один пол
                    el1 *= 10  # подгоняем под размеры
                    pygame.draw.line(screen, 'red', (el1 - 10, k), (el1 + 10, k))
            if rise_x_y:  # рисуем зеленый квадрат(рис)
                for y in rise_x_y:
                    for el in rise_x_y[y]:
                        pygame.draw.rect(screen, 'green', (int(el), int(y), 5, 5))
            k += 20
        screen.blit(player, (x_pos, y_pos))
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            x_pos += v * clock.tick() / 1000
        elif key[pygame.K_a]:
            x_pos -= v * clock.tick() / 1000
        elif key[pygame.K_w]:
            y_pos -= v * clock.tick() / 1000
        elif key[pygame.K_s]:
            y_pos += v * clock.tick() / 1000
        # проверка на то попал ли игрок в рис, если да - удаляем из словаря этот рис
        # простым языком проверка на то коснулся ли он риса, если да - удаляем с карты
        # {180: [50], 280: [50, 90], 380: [150, 260], 600: [150, 220]}
        for el in rise_x_y:
            if el - 20 <= y_pos <= el:
                for qw in rise_x_y[el]:
                    if qw - 20 <= x_pos <= qw:
                        rise_x_y[el].remove(qw)
                        Music().pause()
                        Music().nyam_nyam()
                        # НЕ БАГ А ФИЧА !!!!!!!!!!!!!
                        for i in range(1000):
                            s = 100 - 12 * 12 + 3
                        Music().background_music('Музыка на фон.mp3')
                        rise_result += 1
                        textsurface = myfont.render(f'Количество риса: {rise_result}', False, 'blue')
                        screen.blit(textsurface, (600, 0))
        pygame.display.flip()
    pygame.quit()
