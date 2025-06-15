import pygame
import os
import sys


is_paused = False

def quit_game():
    pygame.quit()
    sys.exit()


def set_paused(paused):
    global is_paused
    is_paused = paused

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)