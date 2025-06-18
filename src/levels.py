LEVELS = {
    1: {
        "background": "images/levels/layer-1.png",
        "ground_image": "images/levels/layer-2.png",
        "platforms": [
            {"x": 10, "y": 601, "width": 150, "height": 30, "image": "images/levels/tile.png"},
            {"x": 200, "y": 500, "width": 150, "height": 30, "image": "images/levels/tile.png"},
            {"x": 10, "y": 400, "width": 150, "height": 30, "image": "images/levels/tile.png"},
            {"x": 200, "y": 300, "width": 150, "height": 30, "image": "images/levels/tile.png"},
            {"x": 430, "y": 200, "width": 150, "height": 30, "image": "images/levels/tile.png"},
            {"x": 775, "y": 390, "width": 150, "height": 30, "image": "images/levels/tile.png"},
            {"x": 850, "y": 290, "width": 150, "height": 30, "image": "images/levels/tile.png"}
        ],
        "enemies": [
            {"x": 475, "y": 653, "move_range": 950, "speed": 4},
        ],
        "carrots": [(10, 250), (310, 430), (480, 125), (980, 615)],
        "finish": (930, 205),
        "finish_images": ["images/finish_0.png", "images/finish_1.png", "images/finish_2.png",
                         "images/finish_3.png", "images/finish_4.png"],
        "music": "sounds/level1_music.ogg",

    },
    2: {
        "background": "images/levels/bg_snow.png",
        "ground_image": "images/levels/Plattform schnee.png",
        "platforms": [
            {"x": 100, "y": 590, "width": 200, "height": 40, "image": "images/levels/Plattform schnee.png"},
            {"x": 400, "y": 490, "width": 150, "height": 40, "image": "images/levels/Plattform schnee.png"},
            {"x": 600, "y": 390, "width": 150, "height": 40, "image": "images/levels/Plattform schnee.png"},
            {"x": 400, "y": 290, "width": 150, "height": 40, "image": "images/levels/Plattform schnee.png"},
            {"x": 220, "y": 190, "width": 100, "height": 40, "image": "images/levels/Plattform schnee.png"},
            {"x": 15, "y": 290, "width": 150, "height": 40, "image": "images/levels/Plattform schnee.png"},
            {"x": 830, "y": 290, "width": 150, "height": 40, "image": "images/levels/Plattform schnee.png"},
        ],
        "enemies": [
            {"x": 475, "y": 653, "move_range": 950, "speed": 4},
        ],
        "carrots": [(0, 650), (15, 265), (1000, 670), (440, 465)],
        "finish": (900, 203),
        "finish_images": ["images/finish_0.png", "images/finish_1.png", "images/finish_2.png",
                         "images/finish_3.png", "images/finish_4.png"],
        "music": "sounds/level2_music.mp3",
    },
    3: {
        "background": "images/levels/voodoo_cactus_underwater.jpg",
        "ground_image": "images/levels/Untitled-2.jpg",
        "platforms": [
            {"x": 55, "y": 615, "width": 75, "height": 75, "image": "images/levels/RTS_Crate.png"},
            {"x": 200, "y": 515, "width": 75, "height": 75, "image": "images/levels/RTS_Crate.png"},
            {"x": 345, "y": 415, "width": 75, "height": 75, "image": "images/levels/RTS_Crate.png"},
            {"x": 200, "y": 315, "width": 75, "height": 75, "image": "images/levels/RTS_Crate.png"},
            {"x": 55, "y": 215, "width": 75, "height": 75, "image": "images/levels/RTS_Crate.png"},
            {"x": 490, "y": 315, "width": 75, "height": 75, "image": "images/levels/RTS_Crate.png"},
            {"x": 200, "y": 315, "width": 75, "height": 75, "image": "images/levels/RTS_Crate.png"},
        ],
        "enemies": [
            {"x": 475, "y": 653, "move_range": 950, "speed": 4},
        ],
        "carrots": [(75, 190), (510, 290), (950, 660)],
        "finish": (970, 605),
        "finish_images": ["images/finish_0.png", "images/finish_1.png", "images/finish_2.png",
                         "images/finish_3.png", "images/finish_4.png"],
        "music": "sounds/level3_music.mp3",
    },
    4: {
        "background": "images/levels/hell_background.jpg",
        "ground_image": "images/levels/LavaTile set.png",
        "platforms": [
            {"x": 100000, "y": 10000, "width": 150, "height": 40, "image": "images/levels/LavaTile set.png"}
        ],
        "boss": {
            "x": 500,             # Позиция босса по горизонтали
            "y": 540,             # Позиция босса по вертикали
            "health": 10,         # Здоровье босса
            "move_range": 300,    # На сколько пикселей босс может уйти от своей начальной позиции
            "speed": 3            # Скорость передвижения босса
        },
        "carrots": [(100000, 10000), (10000, 10000)],
        "finish": (100000, 10000),
        "finish_images": ["images/finish_0.png", "images/finish_1.png", "images/finish_2.png",
                         "images/finish_3.png", "images/finish_4.png"],
        "music": "sounds/level4_music.ogg",
    },
}