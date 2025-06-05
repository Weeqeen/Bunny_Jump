import pygame
import sys
import os
import json
import random

from src.Player import Player
from src.load_image import load_image
from src.levels import LEVELS
from src.Platforms import Platform_Ground, FinishSprite
from src.Draw_t_and_b import draw_text, draw_button
from src.audio_manager import AudioManager
from src.Small_func import quit_game, set_paused
from src.Coin import Coin


# Инициализация Pygame
pygame.init()

# Загрузка настроек
with open('settings.json', 'r') as f:
    SETTINGS = json.load(f)

# Константы
WIDTH, HEIGHT = SETTINGS['resolution']
SKY = (135, 206, 235)
FONT_COLOR = (255, 255, 255)

# Шрифты
font = pygame.font.SysFont(None, 30)
button_font = pygame.font.Font(None, 30)


def random_level():
    return random.randint(1, 5)


def end_menu(screen):
    clock = pygame.time.Clock()
    running = True

    bg_path = load_image("images/end_menu_background.png", scale_factor=1)

    bg = pygame.image.load(bg_path)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 200))

    while running:
        screen.blit(bg, (0, 0))
        draw_text('Поздравляем, вы прошли игру!', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        draw_button('Новая игра', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2, 260, 60,
                    action=lambda: start_new_game(screen), hover_color=(0, 200, 0), default_color=(0, 153, 0))

        draw_button('Выход', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 90, 260, 60,
                    action=quit_game, hover_color=(200, 0, 0), default_color=(153, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)


def pause_menu(screen):
    clock = pygame.time.Clock()
    paused = True

    bg_path = load_image("images/pause_menu_background.png", scale_factor=1)
    bg = pygame.image.load(bg_path)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 200))

    while paused:
        screen.blit(bg, (0, 0))
        draw_text('Пауза', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        draw_button('Продолжить', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 - 50, 260, 60,
                    action=lambda: set_paused(False), hover_color=(100, 200, 100), default_color=(0, 153, 0))

        draw_button('Выход', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 75, 260, 60,
                    action=quit_game, hover_color=(200, 0, 0), default_color=(153, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)


def next_level_screen(screen, level):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 30)

    # Загружаем фон через load_image
    bg = load_image("images/end_menu_background.png", scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT+200))

    # Создаём поверхность для затемнения
    fade_surface = pygame.Surface((WIDTH, HEIGHT+200))
    fade_surface.fill((0, 0, 0))  # Чёрный фон
    fade_surface.set_alpha(0)  # Начинаем с прозрачности

    # Сообщение игроку
    instruction_text = "Нажмите любую клавишу или мышь, чтобы продолжить"
    showing_instruction = False
    instruction_timer = pygame.time.get_ticks() + 1500  # Показываем подсказку через 1.5 секунды

    running = True
    while running:
        now = pygame.time.get_ticks()
        screen.blit(bg, (0, 0))

        # Анимация затухания фона
        for alpha in range(0, 255, 10):
            if not showing_instruction:
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                draw_text(f"Уровень {level}", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(30)
                if alpha >= 250:
                    showing_instruction = True

        if showing_instruction:
            fade_surface.set_alpha(255)
            screen.blit(fade_surface, (0, 0))
            draw_text(f"Уровень {level}", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2 - 40)
            if now > instruction_timer:
                draw_text(instruction_text, small_font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2 + 40)

        pygame.display.flip()

        # Ждём нажатия
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False  # Выходим из цикла и переходим к следующему уровню
                return

        clock.tick(60)


def start_new_game(screen):
    game_loop(screen, level=1)



# Game_loop.py

def game_loop(screen, level):
    all_sprites = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()

    # Игрок
    player = Player(WIDTH // 2, HEIGHT + 40, WIDTH, HEIGHT)
    all_sprites.add(player)

    # Аудио
    audio_manager = AudioManager()
    audio_manager.load_music("in_game_music.mp3")
    audio_manager.set_music_volume(SETTINGS['music_volume'])
    audio_manager.play_music(loops=-1)

    jump_sound = audio_manager.load_sound("jump_sound.wav")
    walk_sound = audio_manager.load_sound("walk_sound.wav")
    coin_sound = audio_manager.load_sound("coin_pickup.wav")
    head_hit_sound = audio_manager.load_sound("head_hit.wav")
    level_complete_sound = audio_manager.load_sound("level_complete.wav")
    game_complete_sound = audio_manager.load_sound("game_complete.mp3")

    # Фон
    bg_path = "images/layer-1.png"
    bg = load_image(bg_path, scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 50))

    # Основная платформа земли
    ground = Platform_Ground(0, HEIGHT + 40, WIDTH + 100, 100, "images/layer-2.png")
    all_sprites.add(ground)

    # Загрузка уровня
    try:
        level_data = LEVELS[level]
    except KeyError:
        print(f"Уровень {level} не найден.")
        return

    platforms = pygame.sprite.Group()
    platforms.add(ground)

    # Добавляем платформы
    for platform in level_data["platforms"]:
        all_sprites.add(platform)
        platforms.add(platform)

    # Добавляем монеты
    for x, y in level_data["coins"]:
        coin = Coin(x, y)
        all_sprites.add(coin)
        coins_group.add(coin)

    # Добавляем финиш
    finish_sprite = FinishSprite(*level_data["finish"], os.path.join("images", "finish_image.jpg"))
    all_sprites.add(finish_sprite)

    running = True
    clock = pygame.time.Clock()
    is_paused = False
    start_time = pygame.time.get_ticks()
    coins_collected = 0

    while running:
        clock.tick(60)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    player.jump()
                    audio_manager.play_sound(jump_sound)
                if event.key == pygame.K_LEFT:
                    player.x_speed = -5
                    audio_manager.play_sound(walk_sound)
                if event.key == pygame.K_RIGHT:
                    player.x_speed = 5
                    audio_manager.play_sound(walk_sound)
                if event.key == pygame.K_DOWN:
                    player.drop_down()
                if event.key == pygame.K_ESCAPE:
                    set_paused(True)
                    pause_menu(screen)
                    set_paused(False)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.x_speed = 0

        if not is_paused:
            # Обновление игрока и спрайтов
            all_sprites.update(platforms)

            # Сбор монет
            collected = pygame.sprite.spritecollide(player, coins_group, True)
            if collected:
                coins_collected += len(collected)
                audio_manager.play_sound(coin_sound)

            # Проверка столкновения с финишем
            if finish_sprite and pygame.sprite.collide_rect(player, finish_sprite):
                audio_manager.play_sound(level_complete_sound)
                if level == 5:
                    audio_manager.play_sound(game_complete_sound)
                    running = False
                    end_menu(screen)
                else:
                    next_level_screen(screen, level + 1)
                    game_loop(screen, level + 1)
                    return

            # Рендеринг
            screen.blit(bg, (0, 0))
            draw_text(f"Уровень: {level}", font, FONT_COLOR, screen, 20, 10, center=False)
            draw_text(f"Время: {int((pygame.time.get_ticks() - start_time) / 1000)}", font, FONT_COLOR, screen,
                      WIDTH - 150, 10, center=False)
            draw_text(f"Монеты: {coins_collected}", font, FONT_COLOR, screen, WIDTH // 2 - 50, 10, center=False)
            all_sprites.draw(screen)
            pygame.display.flip()

    pygame.quit()