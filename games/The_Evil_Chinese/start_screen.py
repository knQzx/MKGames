import random
import re
import time
from music_load import Music  # импорт музыки
import pygame
from menu_load import Button

menushka = True


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


def set_true():
    global menushka
    menushka = True


def setfalse():
    global menushka
    menushka = False

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('The Evil Chinese v.1.0.0')
    size = width, height = 800, 800
    sxr = 30
    screen = pygame.display.set_mode(size)
    # обещание великого правителя
    #Music().rulers_promise('Обещание выдать миску риса.mp3')
    # музыка на фоне
    Music().background_music('Музыка на фон.mp3')
    #
    k = 0
    rise_x_y = {}
    winning_point = []
    '''
    заранее подготавливаем 
    '''
    for el in open('data/levels/level_1/level_1').readlines():
        playeer = Player().player_load(el)  # получаем список координат игрока
        walls = LoadGame().walls_load(el)  # получаем список координат стен
        if not winning_point:
            winning_point = walls
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
    running = True
    clock = pygame.time.Clock()
    v = 100  # пикселей в секунду
    # наш счет
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    rise_result = 0
    '''
    подготавливаем шрифт и размер
    '''
    '''
    всё для менюхи
    '''
    menushka = True


    lvl = False
    clr = [255, 0, 255]
    bg = (255, 255, 0)
    font_size = 15
    font_2 = pygame.font.Font(None, font_size)
    button1 = Button(position=(260, 730), size=(200, 50), clr=(220, 220, 220), cngclr=(255, 0, 0),
                     func=setfalse, text='Start Game')
    button2 = Button((510, 730), (200, 50), (220, 220, 220), (255, 0, 0), print(2), 'Exit')

    button_list = [button1, button2]
    while running:
        if menushka:
            screen.fill(bg)
            x_ppos = 40
            random_list = ['0', '1']
            qwws = 500
            for el in range(8):
                for i in range(25):
                    s = random.choice(random_list)
                    if s == '0':
                        pygame.draw.line(screen, (123, 0, 255),
                                         [x_ppos, qwws],
                                         [x_ppos + 10, qwws], el)
                    x_ppos += 30
                qwws += 20
                x_ppos = 40
            pygame.draw.rect(screen, (123, 0, 255),
                             (260, 140, 70, 370))
            pygame.draw.rect(screen, (123, 100, 255),
                             (335, 140, 10, 250))
            pygame.draw.rect(screen, (123, 100, 255),
                             (335, 400, 10, 110))
            pygame.draw.rect(screen, (123, 100, 255),
                             (360, 140, 100, 370), 6)
            myfont = pygame.font.SysFont('Comic Sans MS', 110)
            textsurface = myfont.render(f'THE EVIL CHINESE', False, 'black')
            screen.blit(textsurface, (60, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for b in button_list:
                            if b.rect.collidepoint(pos):
                                b.call_back()

            for b in button_list:
                b.draw(screen)

            pygame.display.update()
            clock.tick(60)
        else:
            myfont = pygame.font.SysFont('Comic Sans MS', 30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        print(1)
            k = 0
            screen.fill((0, 0, 0))
            '''
            отрисовка количества риса
            '''
            if rise_result >= 0:
                textsurface = myfont.render(f'Количество риса: {rise_result}', False, 'blue')
                screen.blit(textsurface, (550, 0))
            else:
                textsurface = myfont.render(f'Вы должны партии: {abs(rise_result)}', False, 'blue')
                screen.blit(textsurface, (550, 0))
            '''
            отрисовка:
            стен
            стен
            риса
            '''
            for el in open('data/levels/level_1/level_1').readlines():
                walls = LoadGame().walls_load(el)  # получаем список координат стен
                floar = LoadGame().floor_load(el)  # получаем список координат пола
                rise = Rise().rise_load(el)  # получаем список координат риса
                if walls:  # --> если не пустой
                    for el1 in walls:  # проходимся по элементам т.к. может быть не одна стена
                        el1 *= 10  # подгоняем под размеры
                        pygame.draw.line(screen, (254, 0, 0, 255), (el1, k), (el1, k + 20))
                if floar:  # --> если не пустой
                    for el1 in floar:  # проходимся по элементам т.к. может быть не один пол
                        el1 *= 10  # подгоняем под размеры
                        pygame.draw.line(screen, (254, 0, 0, 255), (el1 - 10, k), (el1 + 10, k))
                if rise_x_y:  # рисуем зеленый квадрат(рис)
                    for y in rise_x_y:
                        for el in rise_x_y[y]:
                            pygame.draw.rect(screen, 'green', (int(el), int(y), 5, 5))
                k += 20
            screen.blit(player, (x_pos, y_pos))
            if lvl:
                if rise_result >= 10:
                    win = pygame.image.load('data/achievements/images/partia_gorditsya.png')
                    win = pygame.transform.scale(win, (800, 500))
                    lvl = True
                    screen.blit(win, (0, 30))
                else:
                    win = pygame.image.load('data/disachievements/images/partiya_ne_gorditsya.png')
                    win = pygame.transform.scale(win, (800, 500))
                    lvl = True
                    screen.blit(win, (0, 30))
            '''
            тут у нас реализованы
            нажатия клавиш
            '''
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
                            for i in range(1000):
                                s = 100 - 12 * 12 + 3
                            Music().background_music('Музыка на фон.mp3')
                            rise_result += 1
                            textsurface = myfont.render(f'Количество риса: {rise_result}', False, 'blue')
                            screen.blit(textsurface, (600, 0))
            pygame.display.flip()
            sp = []
            '''
            очень сложный путь определения того
            какой пиксель сейчас под нами, так нужно
            потому что там разброс большой
            '''
            try:
                color = screen.get_at((int(x_pos), int(y_pos)))
                if color == (254, 0, 0, 255) or color == (0, 254, 0, 0):
                    sp.append('Минус один рис')
                color = screen.get_at((int(x_pos + 10), int(y_pos)))
                if color == (254, 0, 0, 255) or color == (0, 254, 0, 0):
                    sp.append('Минус один рис')
                color = screen.get_at((int(x_pos), int(y_pos + 10)))
                if color == (254, 0, 0, 255) or color == (0, 254, 0, 0):
                    sp.append('Минус один рис')
                color = screen.get_at((int(x_pos + 20), int(y_pos + 10)))
                if color == (254, 0, 0, 255) or color == (0, 254, 0, 0):
                    sp.append('Минус один рис')
                color = screen.get_at((int(x_pos + 20), int(y_pos + 20)))
                if color == (254, 0, 0, 255) or color == (0, 254, 0, 0):
                    sp.append('Минус один рис')
                if sp != []:
                    rise_result -= 1
            except IndexError:
                pass
            '''
            проверка на то соответствуют ли
            наши координаты, координатам которые +-
            победные
            '''
            if winning_point[0] * 10 - 15 <= x_pos <= winning_point[0] * 10 + 15:
                if 6 <= y_pos <= 10:
                    '''
                    загружаем картинку в зависимости от того победная она или нет
                    '''
                    lvl = True
                    if rise_result >= 10:
                        win = pygame.image.load('data/achievements/images/partia_gorditsya.png')
                        win = pygame.transform.scale(win, (800, 500))
                        lvl = True
                        screen.blit(win, (0, 30))
                    else:
                        win = pygame.image.load('data/disachievements/images/partiya_ne_gorditsya.png')
                        win = pygame.transform.scale(win, (800, 500))
                        lvl = True
                        screen.blit(win, (0, 30))
            pygame.display.flip()
    pygame.quit()
