import pygame
import sys

is_paused = False  # <-- Добавляем здесь

def quit_game():
    pygame.quit()
    sys.exit()

def set_paused(paused):
    global is_paused
    is_paused = paused

