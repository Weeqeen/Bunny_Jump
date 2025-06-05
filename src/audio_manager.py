import pygame
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()

    def load_music(self, filename):
        self.music_path = os.path.join("sounds", filename)
        pygame.mixer.music.load(self.music_path)

    def play_music(self, loops=-1):
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def load_sound(self, filename):
        path = os.path.join("sounds", filename)
        return pygame.mixer.Sound(path)

    def play_sound(self, sound):
        sound.play()