import pygame
from src.load_image import load_image
from src.Small_func import resource_path


class Carrot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(resource_path("images/carrot.png"), scale_factor=0.08)
        self.rect = self.image.get_rect(topleft=(x, y))