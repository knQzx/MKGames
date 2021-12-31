import time

import pygame


class Music:
    def __init__(self):
        # инициализируем
        pygame.mixer.init()

    def rulers_promise(self, music: str):
        pygame.mixer.music.load(f"data/musics/{music}")
        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)
        # спим, чтобы услышать обещание великого правителя
        time.sleep(9.5)

    def background_music(self, music: str):
        # музыку про социальные кредиты ставим на фон
        pygame.mixer.music.load(f"data/musics/{music}")
        pygame.mixer.music.play(-1)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def nyam_nyam(self):
        song = pygame.mixer.Sound('data/musics/Скушал рис.mp3')
        song.play()
