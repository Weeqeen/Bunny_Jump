import pygame
from src.load_image import load_image


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.images = [
            load_image("images/coin_0.png", scale_factor=0.4),
            load_image("images/coin_45.png", scale_factor=0.4),
            load_image("images/coin_90.png", scale_factor=0.4),
            load_image("images/coin_135.png", scale_factor=0.4),
            load_image("images/coin_180.png", scale_factor=0.4),
            load_image("images/coin_225.png", scale_factor=0.4),
            load_image("images/coin_270.png", scale_factor=0.4),
            load_image("images/coin_315.png", scale_factor=0.4)
        ]

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_index = 0
        self.animation_speed = 100
        self.last_update = pygame.time.get_ticks()

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]