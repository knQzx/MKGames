import os
import sys
import pygame


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
    rect.x, rect.y = screen.get_width() // 2 - image.get_width() // 2,\
        screen.get_height() // 2 - image.get_height() // 2
    screen.blit(image, rect)


def terminate():
    pygame.quit()
    sys.exit()
