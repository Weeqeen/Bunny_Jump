import pygame
import sys
import os
import json
import random

from src.Player import Player
from src.load_image import load_image
from src.levels import LEVELS
from src.Platforms import Platform_Ground, FinishSprite
from src.Draw_t_and_b import draw_text, draw_button, draw_slider, check_slider
from src.audio_manager import AudioManager
from src.Small_func import quit_game, set_paused, is_paused


pygame.init()

with open('settings.json', 'r') as f:
    SETTINGS = json.load(f)

WIDTH, HEIGHT = SETTINGS['resolution']
SKY = (135, 206, 235)
FONT_COLOR = (255, 255, 255)
font = pygame.font.SysFont(None, 30)
button_font = pygame.font.Font(None, 30)


def random_level():
    return random.choice(list(LEVELS.keys()))


def settings_menu(screen, audio_manager):
    global SETTINGS

    clock = pygame.time.Clock()
    music_volume = SETTINGS.get('music_volume', 0.5)
    sound_volume = SETTINGS.get('sound_volume', 0.5)

    original_music_volume = music_volume
    original_sound_volume = sound_volume

    slider_width = 300
    slider_height = 20
    slider_x = WIDTH // 2 - slider_width // 2

    while True:
        screen.fill((0, 0, 0))
        draw_text("Настройки", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 6)

        draw_text("Громкость музыки", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 3 - 30)
        draw_slider(slider_x, HEIGHT // 3, slider_width, slider_height, music_volume, screen)

        draw_text("Громкость звуков", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 3 + 70)
        draw_slider(slider_x, HEIGHT // 3 + 100, slider_width, slider_height, sound_volume, screen)

        if draw_button("Применить", button_font, screen,
                       WIDTH // 2 - 150, HEIGHT - 100, 140, 50,
                       action=lambda: None,
                       hover_color=(0, 200, 255), default_color=(0, 153, 200)):
            SETTINGS['music_volume'] = music_volume
            SETTINGS['sound_volume'] = sound_volume
            with open('settings.json', 'w') as f:
                json.dump(SETTINGS, f, indent=4)
            return

        if draw_button("Отмена", button_font, screen,
                       WIDTH // 2 + 10, HEIGHT - 100, 140, 50,
                       action=lambda: None,
                       hover_color=(200, 200, 200), default_color=(100, 100, 100)):
            audio_manager.set_music_volume(original_music_volume)
            for sound in audio_manager.sounds.values():
                sound.set_volume(original_sound_volume)
            return

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                from src.Small_func import quit_game
                quit_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_slider(slider_x, HEIGHT // 3, slider_width, slider_height, mouse_pos):
                    dragging = 'music'
                elif check_slider(slider_x, HEIGHT // 3 + 100, slider_width, slider_height, mouse_pos):
                    dragging = 'sound'
                else:
                    dragging = None

                if dragging:
                    is_dragging = True
                    while is_dragging:
                        for e in pygame.event.get():
                            if e.type == pygame.MOUSEBUTTONUP:
                                is_dragging = False
                                break

                        if not is_dragging:
                            break

                        new_mouse_pos = pygame.mouse.get_pos()
                        rel_x = max(0, min(slider_width, new_mouse_pos[0] - slider_x))

                        if dragging == 'music':
                            music_volume = rel_x / slider_width
                            audio_manager.set_music_volume(music_volume)
                        else:
                            sound_volume = rel_x / slider_width
                            audio_manager.set_all_sounds_volume(sound_volume)

                        pygame.event.pump()

        pygame.display.flip()
        clock.tick(60)


def main_menu(screen):
    from src.MyGame import Run
    Run()


def end_menu(screen):
    clock = pygame.time.Clock()
    running = True

    bg_raw = load_image("images/end_menu_background.png", scale_factor=1)
    bg = pygame.transform.scale(bg_raw, (WIDTH, HEIGHT + 200))

    while running:
        screen.blit(bg, (0, 0))
        draw_text('Поздравляем, вы прошли игру!', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        if draw_button('Новая игра', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2, 260, 60,
                       action=lambda: start_new_game(screen), hover_color=(0, 200, 0), default_color=(0, 153, 0)):
            pass

        if draw_button('В главное меню', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 90, 260, 60,
                       action=lambda: main_menu(screen), hover_color=(100, 100, 200), default_color=(80, 80, 150)):
            pass

        if draw_button('Выход', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 180, 260, 60,
                       action=quit_game, hover_color=(200, 0, 0), default_color=(153, 0, 0)):
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)


def pause_menu(screen):
    clock = pygame.time.Clock()
    bg_path = load_image("images/pause_menu_background.png", scale_factor=1)
    bg = pygame.transform.scale(bg_path, (WIDTH, HEIGHT + 200))

    button_width = 260
    button_height = 60
    button_x = WIDTH // 2 - button_width // 2

    vertical_spacing = 20
    start_y = HEIGHT // 2 - (button_height + vertical_spacing)

    while True:
        screen.blit(bg, (0, 0))
        draw_text('Пауза', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        if draw_button('Продолжить', button_font, screen,
                       button_x, start_y,
                       button_width, button_height,
                       action=lambda: set_paused(False),
                       hover_color=(100, 200, 100), default_color=(0, 153, 0)):
            break

        if draw_button('В главное меню', button_font, screen,
                       button_x, start_y + button_height + vertical_spacing,
                       button_width, button_height,
                       action=lambda: main_menu(screen),
                       hover_color=(100, 100, 200), default_color=(80, 80, 150)):
            pass

        if draw_button('Выход', button_font, screen,
                       button_x, start_y + 2 * (button_height + vertical_spacing),
                       button_width, button_height,
                       action=quit_game,
                       hover_color=(200, 0, 0), default_color=(153, 0, 0)):
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)


def next_level_screen(screen, level):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 30)

    bg = load_image("images/end_menu_background.png", scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 200))

    fade_surface = pygame.Surface((WIDTH, HEIGHT + 200))
    fade_surface.fill((0, 0, 0))
    fade_surface.set_alpha(0)

    instruction_text = "Нажмите любую клавишу или мышь, чтобы продолжить"
    showing_instruction = False
    instruction_timer = pygame.time.get_ticks() + 1500

    running = True
    while running:
        now = pygame.time.get_ticks()
        screen.blit(bg, (0, 0))

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                running = False
                return

        clock.tick(60)


def start_new_game(screen):
    game_loop(screen, level=1)


def game_loop(screen, level):
    all_sprites = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()

    player = Player(WIDTH // 2, HEIGHT + 40, WIDTH, HEIGHT)
    all_sprites.add(player)

    audio_manager = AudioManager()
    level_data = LEVELS[level]
    music_path = level_data.get("music", "sounds/in_game_music.mp3")
    audio_manager.load_music(music_path)
    audio_manager.set_music_volume(SETTINGS['music_volume'])
    audio_manager.play_music(loops=-1)

    jump_sound = audio_manager.load_sound("jump_sound.wav")
    walk_sound = audio_manager.load_sound("walk_sound.wav")
    coin_sound = audio_manager.load_sound("coin_pickup.wav")
    level_complete_sound = audio_manager.load_sound("level_complete.wav")
    game_complete_sound = audio_manager.load_sound("game_complete.mp3")

    bg_path = level_data["background"]
    bg = load_image(bg_path, scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 50))

    ground_image_path = level_data["ground_image"]
    ground = Platform_Ground(0, HEIGHT + 40, WIDTH + 100, 100, ground_image_path)
    all_sprites.add(ground)
    platforms = pygame.sprite.Group()
    platforms.add(ground)

    for plat in level_data["platforms"]:
        platform = Platform_Ground(
            plat["x"], plat["y"], plat["width"], plat["height"], plat["image"]
        )
        all_sprites.add(platform)
        platforms.add(platform)

    from src.Coin import Coin
    for x, y in level_data["coins"]:
        coin = Coin(x, y)
        all_sprites.add(coin)
        coins_group.add(coin)

    finish_images = level_data.get("finish_images", [])
    finish_sprite = FinishSprite(*level_data["finish"], finish_images)
    all_sprites.add(finish_sprite)

    running = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    coins_collected = 0

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_SPACE]:
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
                    while is_paused:
                        pygame.time.delay(50)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.x_speed = 0

        all_sprites.update(platforms)

        collected = pygame.sprite.spritecollide(player, coins_group, True)
        if collected:
            coins_collected += len(collected)
            audio_manager.play_sound(coin_sound)

        if finish_sprite and pygame.sprite.collide_rect(player, finish_sprite):
            audio_manager.play_sound(level_complete_sound)
            if level == 4:
                audio_manager.play_sound(game_complete_sound)
                running = False
                end_menu(screen)
            else:
                next_level_screen(screen, level + 1)
                game_loop(screen, level + 1)
                return

        screen.blit(bg, (0, 0))
        draw_text(f"Уровень: {level}", font, FONT_COLOR, screen, 20, 10, center=False)
        draw_text(f"Время: {int((pygame.time.get_ticks() - start_time) / 1000)}", font, FONT_COLOR, screen,
                  WIDTH - 150, 10, center=False)
        draw_text(f"Монеты: {coins_collected}", font, FONT_COLOR, screen, WIDTH // 2 - 50, 10, center=False)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()