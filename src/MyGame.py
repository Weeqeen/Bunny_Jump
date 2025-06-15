import pygame
import sys
import os
import json


pygame.init()

SETTINGS = {
    "fullscreen": True,
    "resolution": [
        1024,
        650
    ],
    "music_volume": 0.65,
    "sound_volume": 0.6366666666666667
}
WIDTH, HEIGHT = SETTINGS['resolution']

SKY = (135, 206, 235)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 48
BUTTON_FONT_SIZE = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if SETTINGS['fullscreen'] else 0)

pygame.display.set_caption("Bunny Jump")



icon_path = "images/icon.ico"
if os.path.exists(icon_path):
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

font = pygame.font.SysFont(None, FONT_SIZE)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)

clock = pygame.time.Clock()

from src.load_image import load_image
from src.Game_loop import game_loop, random_level, settings_menu, start_new_game
from src.Small_func import quit_game, resource_path
from src.Draw_t_and_b import draw_text, draw_button
from src.audio_manager import AudioManager



def show_main_menu():
    """Отображает главное меню без рекурсивного запуска Run()"""
    audio_manager = AudioManager()
    audio_manager.load_music(resource_path("sounds/main_menu_music.mp3"))
    audio_manager.set_music_volume(SETTINGS['music_volume'])
    audio_manager.play_music(loops=-1)

    bg_path = os.path.join("images", "main_menu_background.png")
    bg = load_image(resource_path(bg_path), scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 200))

    running = True
    while running:
        screen.blit(bg, (0, 0))
        draw_text('Главное меню', font, FONT_COLOR, screen, WIDTH // 2 + 330, HEIGHT // 4)

        if draw_button('Новая игра', button_font, screen, WIDTH // 2 + 200, HEIGHT // 2 - 50,
                       260, 60, action=lambda: start_new_game(screen),
                       hover_color=(0, 200, 0), default_color=(0, 153, 0)):
            pass

        if draw_button('Рандомный уровень', button_font, screen, WIDTH // 2 + 200, HEIGHT // 2 + 50, 260, 60,
                      action=lambda: game_loop(screen, level=random_level()),
                      hover_color=(255, 200, 0), default_color=(253, 165, 0)):
            pass

        if draw_button('Настройки', button_font, screen, WIDTH // 2 + 200, HEIGHT // 2 + 150, 260, 60,
                      action=lambda: settings_menu(screen, audio_manager),
                      hover_color=(100, 100, 200), default_color=(80, 80, 150)):
            pass

        if draw_button('Выход', button_font, screen, WIDTH // 2 + 200, HEIGHT // 2 + 250, 260, 60,
                      action=quit_game, hover_color=(200, 0, 0), default_color=(153, 0, 0)):
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)


def main_menu(screen):
    """Просто останавливаем музыку и возвращаемся в главное меню"""
    pygame.mixer.music.stop()
    show_main_menu()