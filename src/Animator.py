import pygame


class Animator:
    def __init__(self, images):
        self.images = images
        self.animation_frame = 0
        self.animation_speed = 0.1

    def get_idle(self):
        return self.images["idle"]

    def get_jump_image(self, direction):
        return self.images["jump_right"] if direction == "right" else self.images["jump_left"]

    def get_run_animation(self, direction):
        animation_list = self.images[direction]
        self.animation_frame = (self.animation_frame + self.animation_speed) % len(animation_list)
        frame = animation_list[int(self.animation_frame)]

        fixed_size = (50, 70)
        return pygame.transform.scale(frame, fixed_size)