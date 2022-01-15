import os
import sys
from math import pi, atan, sin, cos

import pygame


def get_sign(num):  # --> return sign of num
    return -1 if num < 0 else 1


def load_image(name, colorkey=None):  # --> load of image with alpha channel
    filename = os.path.join('data', 'images', name)
    # handling the situation if there is no image
    if not os.path.isfile(filename):
        print(f"File with image '{filename}' not found")
        sys.exit()
    # if we have image, we load this is image
    image = pygame.image.load(filename)
    if colorkey is not None:
        # convert image
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        # set colorkey for image
        image.set_colorkey(colorkey)
    else:
        # convert alpha image
        image = image.convert_alpha()
    return image


def draw_background(screen, image):  # --> draw image at screen with accounting of display size
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


def get_screen_coords(screen, rel_pos):  # Return position at screen by relative position
    return screen.get_width() * rel_pos[0], screen.get_height() * rel_pos[1]


def collide_mask_rect(left, right):
    x_offset = right.rect[0] - left.rect[0]
    y_offset = right.rect[1] - left.rect[1]
    try:
        left_mask = left.mask
    except AttributeError:
        left_mask = pygame.mask.Mask(left.size, True)
    try:
        right_mask = right.mask
    except AttributeError:
        right_mask = pygame.mask.Mask(right.size, True)
    return left_mask.overlap(right_mask, (x_offset, y_offset))


def check_collide(sprite: pygame.sprite.Sprite, screen: pygame.surface.Surface,
                  *collide_groups):  # Check to collide with groups and screen framework
    collide = False
    if not sprite.rect.colliderect((0, 0 + sprite.rect.height,
                                    screen.get_width(),
                                    screen.get_height() - sprite.rect.height * 2)):
        return True
    for collide_group in collide_groups:
        for collide_sprite in collide_group:
            if collide_mask_rect(sprite, collide_sprite):
                collide = True
                break
        if collide:
            break
    return collide


def move_sprite(sprite: pygame.sprite.Sprite, d_coords, screen: pygame.surface.Surface,
                *collide_groups):  # Move sprite with accounting of collisions
    dx, dy = d_coords
    dist = (dx ** 2 + dy ** 2) ** 0.5

    prev_rect = sprite.rect.copy()
    sprite.rect.x, sprite.rect.y = int(sprite.x + dx), int(sprite.y + dy)
    if check_collide(sprite, screen, *collide_groups):
        sprite.rect = prev_rect.copy()
        sprite.rect.y = int(sprite.y - dy)
        if not check_collide(sprite, screen, *collide_groups):
            sprite.y -= dy
            if dy > 0:
                sprite.sheet_state = 0
            sprite.rect.y = int(sprite.y)
            sprite.dy = 0
            sprite.rect.x = int(sprite.x + dx)
        else:
            sprite.rect.x, sprite.rect.y = int(sprite.x + dx), int(sprite.y + dy)
    if not check_collide(sprite, screen, *collide_groups):
        sprite.x += dx
        sprite.y += dy
        return {'d_coords': (dx, dy), 'sprite_move': True}
    sprite.rect = prev_rect.copy()
    if sprite.dy == 0:
        sprite.rect.y = int(sprite.y)

    start_angle = atan(dy / dx)
    collide_perms = [{'d_angle': pi / 2, 'prev_ch_d_angle': pi / 2, 'prev_result': False},
                     {'d_angle': -pi / 2, 'prev_ch_d_angle': -pi / 2, 'prev_result': False}]

    ITER_COUNT = 6
    for _ in range(ITER_COUNT):
        for collide_perm in collide_perms:
            if not collide_perm['prev_result']:
                d_angle = get_sign(collide_perm['d_angle']) * \
                          (abs(collide_perm['d_angle']) - abs(collide_perm['prev_ch_d_angle'] / 2))
            else:
                d_angle = get_sign(collide_perm['d_angle']) * \
                          min((abs(collide_perm['d_angle']) + abs(collide_perm['prev_ch_d_angle'])),
                              pi / 2)
            angle = start_angle + d_angle
            sprite.rect.x, sprite.rect.y = int(sprite.x + cos(angle) * dist), \
                int(sprite.y + sin(angle) * dist)
            if collide_perm['prev_result']:
                collide_perm['prev_ch_d_angle'] = collide_perm['prev_ch_d_angle'] / 2
            else:
                collide_perm['prev_ch_d_angle'] = abs(d_angle) - abs(collide_perm['d_angle'])
            collide_perm['d_angle'] = d_angle
            collide_perm['prev_result'] = check_collide(sprite, screen, *collide_groups)
            sprite.rect = prev_rect.copy()
        if len(collide_perms) == 2:
            if collide_perms[0]['prev_result'] != collide_perms[1]['prev_result']:
                collide_perms = list(filter(lambda elem: not elem['prev_result'], collide_perms))
    collide_perm = collide_perms[0]
    if collide_perms[0]['prev_result']:
        d_angle = get_sign(collide_perm['d_angle']) * (
                abs(collide_perm['d_angle']) + abs(collide_perm['prev_ch_d_angle']))
    else:
        d_angle = collide_perm['d_angle']
    angle = start_angle + d_angle
    sprite.x, sprite.y = sprite.x + cos(angle) * dist, sprite.y + sin(angle) * dist
    sprite.rect.x, sprite.rect.y = int(sprite.x), int(sprite.y)
    if check_collide(sprite, screen, *collide_groups):
        sprite.rect = prev_rect.copy()
        sprite.x, sprite.y = sprite.rect.x, sprite.rect.y
        return {'d_coords': (0, 0), 'sprite_move': False}
    return {'d_coords': (cos(angle) * dist, sin(angle) * dist), 'sprite_move': True}


def terminate():  # Function break the program
    pygame.quit()
    sys.exit()
