import pygame
import os
from src.Small_func import resource_path


class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.sound_volume = 0.5

    def load_music(self, filename):
        self.music_path = filename
        pygame.mixer.music.load(resource_path(self.music_path))

    def play_music(self, loops=-1):
        pygame.mixer.music.play(loops)

    def play_sound(self, sound):
        sound.play()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def load_sound(self, filename):
        path = os.path.join("sounds", filename)
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.sound_volume)
        self.sounds[filename] = sound
        return sound

    def set_all_sounds_volume(self, volume):
        self.sound_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def stop_all_sounds(self):
        for sound in self.sounds.values():
            sound.stop()