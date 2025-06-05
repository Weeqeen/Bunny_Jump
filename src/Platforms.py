import pygame
from src.load_image import load_image

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 200, 0))  # зелёная платформа по умолчанию
        self.rect = self.image.get_rect(topleft=(x, y))

class Platform_Ground(Platform):
    def __init__(self, x, y, width, height, sprite_path):
        super().__init__(x, y, width, height)
        self.image = load_image(sprite_path, scale_factor=1)  # sprite_path — это строка с путём
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

class FinishSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = load_image(image_path, scale_factor=0.2)
        self.rect = self.image.get_rect(topleft=(x, y))