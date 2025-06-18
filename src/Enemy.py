import pygame
from src.load_image import load_image
from src.Small_func import resource_path


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, move_range=200, speed=2):
        super().__init__()

        # Загрузка спрайтов
        self.idle_image_left = load_image(resource_path("images/fox_standing.png"), scale_factor=1)
        self.run_images_left = [
            load_image(resource_path("images/fox_run_1.png"), scale_factor=0.7),
            load_image(resource_path("images/fox_run_2.png"), scale_factor=0.7)
        ]

        # Создание зеркальных спрайтов для движения влево
        self.idle_image_right = pygame.transform.flip(self.idle_image_left, True, False)
        self.run_images_right = [pygame.transform.flip(img, True, False) for img in self.run_images_left]

        # Активное изображение
        self.image = self.idle_image_right
        self.rect = self.image.get_rect(topleft=(x, y))

        # Параметры движения
        self.start_x = x
        self.move_range = move_range  # Дистанция, на которую может двигаться враг
        self.speed = speed
        self.direction = 1  # 1 - вправо, -1 - влево

        # Границы
        self.left_bound = x - move_range // 2
        self.right_bound = x + move_range // 2

        # Анимационные параметры
        self.animation_frame = 0
        self.animation_speed = 0.1  # Скорость анимации

    def update(self, *args):
        # Обновление позиции
        self.rect.x += self.speed * self.direction

        # Смена направления, если достигнут край
        if self.rect.x <= self.left_bound or self.rect.x >= self.right_bound:
            self.direction *= -1

        # Выбор спрайтов в зависимости от направления
        if self.direction > 0:
            idle_image = self.idle_image_right
            run_images = self.run_images_right
        else:
            idle_image = self.idle_image_left
            run_images = self.run_images_left

        # Анимация бега
        if self.direction != 0:
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(run_images)
            self.image = run_images[int(self.animation_frame)]
        else:
            self.image = idle_image

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, move_range=200, speed=2, health=10):
        super().__init__()

        self.idle_images_left = [
            load_image(resource_path(f"images/boss/demon_idle_{i}-no-bg-preview (carve.photos).png"), scale_factor=1.5)
            for i in range(1, 7)
        ]
        self.run_images_left = [
            load_image(resource_path(f"images/boss/demon_walk_{i}-no-bg-preview (carve.photos).png"), scale_factor=1.5)
            for i in range(1, 13)
        ]

        # Создание зеркальных спрайтов для движения вправо
        self.idle_images_right = [pygame.transform.flip(img, True, False) for img in self.idle_images_left]
        self.run_images_right = [pygame.transform.flip(img, True, False) for img in self.run_images_left]

        # <<< Загрузка кадров смерти >>>
        self.death_frames_left = [
            load_image(resource_path(f"images/boss/demon_death_{i}-no-bg-preview (carve.photos).png"), scale_factor=1.5)
            for i in range(1, 23)
        ]
        self.death_frames_right = [pygame.transform.flip(img, True, False) for img in self.death_frames_left]

        # Активное изображение
        self.image = self.idle_images_right[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.last_hit_time = 0
        # Параметры движения
        self.start_x = x
        self.move_range = move_range
        self.speed = speed
        self.direction = 1  # 1 - вправо, -1 - влево

        # Границы
        self.left_bound = x - move_range // 2
        self.right_bound = x + move_range // 2

        # Анимационные параметры
        self.animation_frame = 0
        self.animation_speed = 0.15  # скорость анимации

        # Здоровье босса
        self.health = health
        self.max_health = health

        # Для получения урона
        self.hit = False
        self.hit_timer = 0
        self.hit_duration = 15  # длительность эффекта получения урона

    def update(self, player_rect=None):
        print(f"[DEBUG] Обновление босса. HP: {self.health}, Rect: {self.rect}")

        # <<< Логика смерти и анимации >>>
        if self.health <= 0:
            death_frames = self.death_frames_right if self.direction == 1 else self.death_frames_left
            self.animation_frame += self.animation_speed
            animation_index = int(self.animation_frame)

            if animation_index < len(death_frames):
                self.image = death_frames[animation_index]
            else:
                self.image = death_frames[-1]
                self.kill()  # Убираем босса после окончания анимации

            return

        # <<< ОСНОВНОЕ ПОВЕДЕНИЕ (движение и анимация) >>>
        # Движение босса туда-сюда
        self.rect.x += self.speed * self.direction

        if self.rect.x <= self.left_bound or self.rect.x >= self.right_bound:
            self.direction *= -1

        # Выбор спрайтов в зависимости от направления
        if self.direction > 0:
            idle_images = self.idle_images_right
            run_images = self.run_images_right
        else:
            idle_images = self.idle_images_left
            run_images = self.run_images_left

        # Анимация ходьбы или стояния
        if self.direction != 0:
            self.animation_frame += self.animation_speed
            animation_index = int(self.animation_frame)
            if animation_index < len(run_images):
                self.image = run_images[animation_index]
            else:
                self.image = run_images[animation_index % len(run_images)]
        else:
            self.animation_frame = 0
            self.image = idle_images[0]

        # Эффект получения урона
        if self.hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.hit = False

    def take_damage(self):
        """Метод для нанесения урона боссу"""
        if self.health > 0:
            self.health -= 1
            print(f"[DEBUG] HP босса: {self.health}")
            self.hit = True
            self.hit_timer = self.hit_duration

            if self.health <= 0:
                self.animation_frame = 0  # Сброс анимации перед смертью

    def draw(self, surface):
        # Отрисовка босса
        surface.blit(self.image, self.rect.topleft)

        # Визуальный эффект получения урона (мигание)
        if self.hit and self.hit_timer % 2 == 0:
            surface.blit(self.image, self.rect.topleft)

        # Отображение здоровья босса
        if self.health > 0:
            font = pygame.font.Font(None, 36)
            health_text = font.render(f"Босс: {self.health} HP", True, (255, 0, 0))
            surface.blit(health_text, (self.rect.centerx - 60, self.rect.top - 30))