import os
import sys
import pygame


def load_level(name):
    filename = os.path.join('data', 'levels', name)
    with open(filename, 'r') as map_file:
        level_map = [line.strip() for line in map_file]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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


def terminate():
    pygame.quit()
    sys.exit()
