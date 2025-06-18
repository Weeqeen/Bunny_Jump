import pygame
from src.load_image import load_image
from src.Small_func import resource_path
from src.Animator import Animator


class Player(pygame.sprite.Sprite):
    MAX_SPEED = 5
    GRAVITY = 1
    JUMP_FORCE = -15

    def __init__(self, x, y, width, height):
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
        self.animator = Animator(self.images)
        self.image = self.animator.get_idle()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self._x_speed = 0
        self._y_speed = 0
        self._gravity = self.GRAVITY
        self._is_jumping = False
        self._direction = "right"
        self.WIDTH = width
        self.HEIGHT = height

    @property
    def x_speed(self):
        return self._x_speed

    @x_speed.setter
    def x_speed(self, value):
        if abs(value) > self.MAX_SPEED:
            raise ValueError(f"Скорость не может превышать {self.MAX_SPEED}")
        self._x_speed = value

    @property
    def y_speed(self):
        return self._y_speed

    @y_speed.setter
    def y_speed(self, value):
        self._y_speed = value

    @property
    def is_jumping(self):
        return self._is_jumping

    @property
    def direction(self):
        return self._direction

    def set_x_speed(self, value):
        """Установка горизонтальной скорости с ограничением"""
        if abs(value) > self.MAX_SPEED:
            raise ValueError(f"Скорость не может превышать {self.MAX_SPEED}")
        self._x_speed = value

    def set_y_speed(self, value):
        self._y_speed = value

    def set_is_jumping(self, value):
        self._is_jumping = value

    def set_direction(self, value):
        if value not in ("left", "right"):
            raise ValueError("Направление должно быть 'left' или 'right'")
        self._direction = value

    def update(self, platforms):
        self.rect.x += self._x_speed
        prev_y = self.rect.y
        self._y_speed += self._gravity
        self.rect.y += self._y_speed
        self._is_jumping = self._y_speed != 0
        self._handle_collisions(platforms, prev_y)
        self._apply_boundaries()
        self.animate()

    def _handle_collisions(self, platforms, prev_y):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if prev_y + self.rect.height <= platform.rect.top:
                self.rect.bottom = platform.rect.top
                self._y_speed = 0
                self._is_jumping = False
            elif prev_y >= platform.rect.bottom:
                self.rect.top = platform.rect.bottom
                self._y_speed = 0
            else:
                if self._x_speed > 0:
                    self.rect.right = platform.rect.left
                elif self._x_speed < 0:
                    self.rect.left = platform.rect.right

    def _apply_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH
        if self.rect.bottom > self.HEIGHT + 150:
            self.rect.bottom = self.HEIGHT + 150
            self._y_speed = 0
            self._is_jumping = False

    def animate(self):
        if self._is_jumping:
            self.image = self.animator.get_jump_image(self._direction)
        elif self._x_speed > 0:
            self._direction = "right"
            self.image = self.animator.get_run_animation("right")
        elif self._x_speed < 0:
            self._direction = "left"
            self.image = self.animator.get_run_animation("left")
        else:
            self.image = self.animator.get_idle()

    def jump(self):
        if not self._is_jumping:
            self._y_speed = self.JUMP_FORCE
            self._is_jumping = True

    def drop_down(self):
        self._y_speed = 10