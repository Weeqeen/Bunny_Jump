import pygame

def load_image(path, scale_factor=1.0):
    image = pygame.image.load(path).convert_alpha()
    width = int(image.get_width() * scale_factor)
    height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (width, height))