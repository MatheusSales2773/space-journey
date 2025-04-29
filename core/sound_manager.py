import pygame

class SoundManager:
    @staticmethod
    def init():
        pygame.mixer.init()

    @staticmethod
    def play_soundtrack(url, loop = -1 , volume = 0.5):
        pygame.mixer.music.load(url)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()