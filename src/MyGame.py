import pygame
import sys
import os
from src.load_image import load_image
from src.Game_loop import game_loop, random_level
from src.Small_func import quit_game
from src.Draw_t_and_b import draw_text, draw_button
from src.audio_manager import AudioManager

# Настройки из JSON
import json
with open('settings.json', 'r') as f:
    SETTINGS = json.load(f)

WIDTH, HEIGHT = SETTINGS['resolution']
SKY = (135, 206, 235)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 48
BUTTON_FONT_SIZE = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if SETTINGS['fullscreen'] else 0)
pygame.display.set_caption("Jump 'n' Run")
font = pygame.font.SysFont(None, FONT_SIZE)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
clock = pygame.time.Clock()

def Run():
    running = True
    audio_manager = AudioManager()
    audio_manager.load_music("main_menu_music.mp3")
    audio_manager.set_music_volume(SETTINGS['music_volume'])
    audio_manager.play_music(loops=-1)

    # Загрузка и масштабирование фона

    bg_path = os.path.join("images", "main_menu_background.png")
    bg = load_image(bg_path, scale_factor=1)  # Загружаем фон
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT+200))  # Растягиваем на размер экрана

    while running:
        screen.blit(bg, (0, 0))  # Отображаем фон с координатами (0, 0)
        draw_text('Главное меню', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        draw_button('Новая игра', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 - 50,
                    260, 60, action=lambda: game_loop(screen, level=1),
                    hover_color=(0, 200, 0), default_color=(0, 153, 0))

        draw_button('Рандомный уровень', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 50, 260, 60,
                    action=lambda: game_loop(screen, level=random_level()),
                    hover_color=(255, 200, 0), default_color=(253, 165, 0))

        draw_button('Выход', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 150, 260, 60, quit_game,
                    hover_color=(200, 0, 0), default_color=(153, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)