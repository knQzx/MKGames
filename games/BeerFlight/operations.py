import os
import sys
import pygame
from math import pi, atan, sin, cos


def get_sign(num):
    return -1 if num < 0 else 1


def load_image(name, colorkey=None):
    filename = os.path.join('data', 'images', name)
    if not os.path.isfile(filename):
        print(f"File with image '{filename}' not found")
        sys.exit()
    image = pygame.image.load(filename)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_background(screen, image):
    image_ratio = image.get_width() / image.get_height()
    screen_ratio = screen.get_width() / screen.get_height()
    if image_ratio > screen_ratio:
        new_image_size = screen.get_height() * image_ratio, screen.get_height()
    else:
        new_image_size = screen.get_width(), 1 / image_ratio / image.get_width()
    image = pygame.transform.scale(image, new_image_size)
    rect = image.get_rect()
    rect.x, rect.y = screen.get_width() // 2 - image.get_width() // 2, \
                     screen.get_height() // 2 - image.get_height() // 2
    screen.blit(image, rect)


def get_screen_coords(screen, rel_pos):
    return screen.get_width() * rel_pos[0], screen.get_height() * rel_pos[1]


def check_collide(sprite: pygame.sprite.Sprite, *collide_groups):
    collide = False
    for collide_group in collide_groups:
        for collide_sprite in collide_group:
            if pygame.sprite.collide_mask(sprite, collide_sprite):
                collide = True
                break
        if collide:
            break
    return collide


def move_sprite(sprite: pygame.sprite.Sprite, d_coords, *collide_groups):
    dx, dy = d_coords
    dist = (dx ** 2 + dy ** 2) ** 0.5

    prev_rect = sprite.rect.copy()
    sprite.x, sprite.y = sprite.x + dx, sprite.y + dy
    sprite.rect.x, sprite.rect.y = int(sprite.x), int(sprite.y)
    if not check_collide(sprite, *collide_groups):
        return {'collide': False, 'sprite_move': True}
    sprite.rect = prev_rect.copy()

    start_angle = atan(dy / dx)
    collide_perms = [{'angle': -pi / 2, 'prev_d_angle': -pi / 2, 'prev_result': False}]

    ITER_COUNT = 6
    for _ in range(ITER_COUNT):
        for collide_perm in collide_perms:
            if not collide_perm['prev_result']:
                d_angle = get_sign(collide_perm['angle']) * \
                          (abs(collide_perm['angle']) - abs(collide_perm['prev_d_angle'] / 2))
            else:
                d_angle = get_sign(collide_perm['angle']) * \
                          min((abs(collide_perm['angle']) + abs(collide_perm['prev_d_angle'])), pi / 2)
            angle = start_angle + d_angle
            sprite.rect.x, sprite.rect.y = int(sprite.x + cos(angle) * dist), \
                int(sprite.y + sin(angle) * dist)
            collide_perm['angle'] = angle
            if collide_perm['prev_result']:
                d_angle /= 2
            collide_perm['prev_d_angle'] = d_angle
            collide_perm['prev_result'] = check_collide(sprite, *collide_groups)
            sprite.rect = prev_rect.copy()
        if len(collide_perms) == 2:
            if collide_perms[0]['prev_result'] != collide_perms[1]['prev_result']:
                collide_perms = list(filter(lambda elem: not elem['prev_result'], collide_perms))
    collide_perm = collide_perms[0]
    if collide_perms[0]['prev_result']:
        d_angle = get_sign(collide_perm['angle']) * (abs(collide_perm['angle']) + abs(collide_perm['prev_d_angle']))
    else:
        d_angle = collide_perm['angle']
    angle = start_angle + d_angle
    sprite.x, sprite.y = sprite.x + cos(angle) * dist, sprite.y + sin(angle) * dist
    sprite.rect.x, sprite.rect.y = int(sprite.x), int(sprite.y)
    if check_collide(sprite, *collide_groups):
        sprite.rect = prev_rect.copy()
        sprite.x, sprite.y = sprite.rect.x, sprite.rect.y
        return {'collide': True, 'sprite_move': False}
    return {'collide': True, 'sprite_move': True}


def terminate():
    pygame.quit()
    sys.exit()
