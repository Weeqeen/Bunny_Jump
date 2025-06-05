import pygame
from src.load_image import load_image


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(topleft=(x, y))


class Platform_Ground(Platform):
    def __init__(self, x, y, width, height, sprite_path):
        super().__init__(x, y, width, height)
        self.image = load_image(sprite_path, scale_factor=1)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


class FinishSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image_paths):
        super().__init__()
        self.images = [load_image(path, scale_factor=1.5) for path in image_paths]
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