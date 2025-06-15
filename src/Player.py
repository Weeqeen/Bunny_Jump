import pygame
from src.load_image import load_image
from src.Small_func import resource_path


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        """
        :param x: Начальная позиция по X
        :param y: Начальная позиция по Y
        :param width: Ширина экрана
        :param height: Высота экрана
        """
        super().__init__()

        scale_factor = 0.8

        self.images = {
            "idle": load_image(resource_path("images/Стойка.png"), scale_factor),
            "right": [
                load_image(resource_path("images/Бег1.png"), scale_factor),
                load_image(resource_path("images/Бег2.png"), scale_factor),
                load_image(resource_path("images/Бег3.png"), scale_factor),
                load_image(resource_path("images/Бег4.png"), scale_factor),
                load_image(resource_path("images/Бег5.png"), scale_factor),
                load_image(resource_path("images/Бег6.png"), scale_factor)
            ],
            "left": [
                pygame.transform.flip(load_image(resource_path("images/Бег1.png"), scale_factor), True, False),
                pygame.transform.flip(load_image(resource_path("images/Бег2.png"), scale_factor), True, False),
                pygame.transform.flip(load_image(resource_path("images/Бег3.png"), scale_factor), True, False),
                pygame.transform.flip(load_image(resource_path("images/Бег4.png"), scale_factor), True, False),
                pygame.transform.flip(load_image(resource_path("images/Бег5.png"), scale_factor), True, False),
                pygame.transform.flip(load_image(resource_path("images/Бег6.png"), scale_factor), True, False)
            ],
            "jump_right": load_image(resource_path("images/Прыжок3.png"), scale_factor),
            "jump_left": pygame.transform.flip(
                load_image(resource_path("images/Прыжок3.png"), scale_factor), True, False),
        }

        self.image = self.images["idle"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self.y_speed = 0
        self.x_speed = 0
        self.gravity = 1
        self.is_jumping = False
        self.direction = "right"
        self.animation_frame = 0
        self.animation_speed = 0.1

        self.WIDTH = width
        self.HEIGHT = height

    def update(self, platforms):
        """Обновление состояния игрока"""
        self.rect.x += self.x_speed

        prev_y = self.rect.y
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        self.is_jumping = self.y_speed != 0

        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if prev_y + self.rect.height <= platform.rect.top:
                self.rect.bottom = platform.rect.top
                self.y_speed = 0
                self.is_jumping = False
            elif prev_y >= platform.rect.bottom:
                self.rect.top = platform.rect.bottom
                self.y_speed = 0
            else:
                if self.x_speed > 0:
                    self.rect.right = platform.rect.left
                elif self.x_speed < 0:
                    self.rect.left = platform.rect.right

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH

        if self.rect.bottom > self.HEIGHT + 70:
            self.rect.bottom = self.HEIGHT + 70
            self.y_speed = 0
            self.is_jumping = False

        self.animate()

    def animate(self):
        """Анимация персонажа"""
        bottom = self.rect.bottom
        x = self.rect.x

        if self.is_jumping:
            self.image = self.images["jump_right"] if self.direction == "right" else self.images["jump_left"]
        elif self.x_speed > 0:
            self.direction = "right"
            animation_list = self.images["right"]
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(animation_list)
            self.image = animation_list[int(self.animation_frame)]
        elif self.x_speed < 0:
            self.direction = "left"
            animation_list = self.images["left"]
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(animation_list)
            self.image = animation_list[int(self.animation_frame)]
        else:
            self.image = self.images["idle"]

        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = x

    def jump(self):
        """Начать прыжок"""
        if not self.is_jumping:
            self.y_speed = -15
            self.is_jumping = True

    def drop_down(self):
        """Спуск вниз сквозь платформы (при нажатии вниз)"""
        self.y_speed = 10