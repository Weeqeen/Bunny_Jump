import os
from src.Platforms import Platform

LEVELS = {
    1: {
        "platforms": [
            Platform(50, 590, 150, 20),
            Platform(200, 500, 150, 20),
            Platform(430, 480, 150, 20),
            Platform(650, 390, 150, 20),
            Platform(800, 300, 150, 20),
        ],
        "coins": [
            (300, 485),
            (600, 400),
        ],
        "finish": (900, 550),  # Сохраняем только координаты
    },
    2: {
        "platforms": [
            Platform(450, 590, 150, 20),
            Platform(250, 500, 150, 20),
            Platform(650, 500, 150, 20),
            Platform(830, 400, 150, 20),
            Platform(150, 220, 150, 20),
            Platform(300, 420, 150, 20),
            Platform(600, 320, 150, 20),
        ],
        "coins": [
            (500, 300),
            (800, 300),
        ],
        "finish": (950, 150),
    }
}