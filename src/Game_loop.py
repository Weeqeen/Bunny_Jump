import pygame
import sys
import os
import random
import pickle

from pygame.mixer_music import set_volume
from src.Player import Player
from src.load_image import load_image
from src.levels import LEVELS
from src.Platforms import Platform_Ground, FinishSprite
from src.Draw_t_and_b import draw_text, draw_button, draw_slider, check_slider
from src.audio_manager import AudioManager
from src.Small_func import quit_game, set_paused, is_paused, resource_path
from src.Enemy import Enemy, Boss



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
FONT_COLOR_blue = (0, 0, 51)
font = pygame.font.SysFont(None, 30)
button_font = pygame.font.Font(None, 30)

total_carrots_collected = 0



def random_level():
    return random.choice(list(LEVELS.keys()))


def save_settings():
    settings = {
        'music_volume': SETTINGS['music_volume'],
        'sound_volume': SETTINGS['sound_volume']
    }
    with open('settings.pkl', 'wb') as f:
        pickle.dump(settings, f)


def load_settings():
    global SETTINGS
    try:
        with open('settings.pkl', 'rb') as f:
            data = f.read()
            if not data:
                raise EOFError("Файл settings.pkl пуст")
            loaded_settings = pickle.loads(data)
            SETTINGS['music_volume'] = loaded_settings.get('music_volume', 0.5)
            SETTINGS['sound_volume'] = loaded_settings.get('sound_volume', 0.5)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        SETTINGS['music_volume'] = 0.5
        SETTINGS['sound_volume'] = 0.5
        save_settings()


load_settings()


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
            save_settings()
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
    from src.MyGame import show_main_menu
    show_main_menu()


def restart_level(screen, level):
    game_loop(screen, level)


def pause_menu(screen, level):
    clock = pygame.time.Clock()
    bg_path = load_image(resource_path("images/pause_menu_background.png"), scale_factor=1)
    bg = pygame.transform.scale(bg_path, (WIDTH, HEIGHT + 120))

    button_width = 260
    button_height = 60
    button_x = WIDTH // 2 - button_width // 2
    vertical_spacing = 20

    while True:
        screen.blit(bg, (0, 0))
        draw_text('Пауза', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        if draw_button('Продолжить', button_font, screen,
                       button_x, HEIGHT // 2 - 100,
                       button_width, button_height,
                       action=lambda: set_paused(False),
                       hover_color=(100, 200, 100), default_color=(0, 153, 0)):
            break

        if draw_button('Перезапустить уровень', button_font, screen,
                       button_x, HEIGHT // 2 - 100 + button_height + vertical_spacing,
                       button_width, button_height,
                       action=lambda: restart_level(screen, level),
                       hover_color=(200, 200, 100), default_color=(180, 180, 50)):
            pass

        if draw_button('В главное меню', button_font, screen,
                       button_x, HEIGHT // 2 - 100 + 2 * (button_height + vertical_spacing),
                       button_width, button_height,
                       action=lambda: main_menu(screen),
                       hover_color=(100, 100, 200), default_color=(80, 80, 150)):
            pass

        if draw_button('Выход', button_font, screen,
                       button_x, HEIGHT // 2 - 100 + 3 * (button_height + vertical_spacing),
                       button_width, button_height,
                       action=quit_game,
                       hover_color=(200, 0, 0), default_color=(153, 0, 0)):
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)


def calculate_stars(carrots_collected, total_carrots, time_taken):
    if total_carrots == 0:
        return 0

    collected_ratio = carrots_collected / total_carrots

    if carrots_collected == total_carrots and time_taken < 30:
        return 3
    elif collected_ratio >= 0.5 and time_taken < 30:
        return 2
    elif carrots_collected == total_carrots and 30 <= time_taken < 45:
        return 2
    elif carrots_collected == total_carrots and time_taken >= 45:
        return 1
    else:
        return 1


def display_stars(surface, stars, x, y):
    STAR_SIZE = 40
    SPACING = 10
    full_star = load_image(resource_path("images/star_full.png"), scale_factor=1)
    empty_star = load_image(resource_path("images/star_empty.png"), scale_factor=1)
    full_star = pygame.transform.scale(full_star, (STAR_SIZE, STAR_SIZE))
    empty_star = pygame.transform.scale(empty_star, (STAR_SIZE, STAR_SIZE))

    for i in range(3):
        if i < stars:
            surface.blit(full_star, (x + i * (STAR_SIZE + SPACING), y))
        else:
            surface.blit(empty_star, (x + i * (STAR_SIZE + SPACING), y))


def next_level_screen(screen, level, total_carrots=0, carrots_collected=0, time_taken=0):
    clock = pygame.time.Clock()
    bg = load_image(resource_path("images/sky3.jpg"), scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 200))

    stars = calculate_stars(carrots_collected, total_carrots, time_taken)

    instruction_text = "Нажмите любую клавишу или мышь, чтобы продолжить"
    running = True

    while running:
        screen.blit(bg, (0, 0))

        draw_text(f"Уровень {level- 1}", font, FONT_COLOR_blue, screen, WIDTH // 2, HEIGHT // 2 - 80)

        draw_text(f"Собрано морковок: {carrots_collected}/{total_carrots}",
                  button_font, FONT_COLOR_blue, screen, WIDTH // 2, HEIGHT // 2 - 20, center=True)
        draw_text(f"Время: {int(time_taken)} секунд",
                  button_font, FONT_COLOR_blue, screen, WIDTH // 2, HEIGHT // 2 + 20, center=True)

        display_stars(screen, stars, x=WIDTH // 2 - 75, y=HEIGHT // 2 + 60)

        draw_text(instruction_text, button_font, FONT_COLOR_blue, screen, WIDTH // 2, HEIGHT // 2 + 140)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                running = False
                return

        pygame.display.flip()
        clock.tick(60)


def start_new_game(screen):
    game_loop(screen, level=1)


def show_victory(screen, audio_manager):
    clock = pygame.time.Clock()
    audio_manager.stop_all_sounds()
    victory_sound = audio_manager.load_sound(resource_path("sounds/victory_music.mp3"))
    audio_manager.play_sound(victory_sound)
    bg = load_image(resource_path("images/end_menu_background.png"), scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 200))

    while True:
        screen.blit(bg, (0, 0))
        draw_text("Поздравляем!", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 3)
        draw_text("Вы собрали достаточно морковок и победили древнего духа.", button_font, FONT_COLOR, screen,
                  WIDTH // 2, HEIGHT // 2, center=True)
        draw_text("Игра окончена", button_font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2 + 40, center=True)
        draw_text("Нажмите любую клавишу, чтобы вернуться в меню", button_font, FONT_COLOR, screen,
                  WIDTH // 2, HEIGHT // 2 + 100, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                audio_manager.stop_all_sounds()
                quit_game()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                audio_manager.stop_all_sounds()
                main_menu(screen)
                return

        pygame.display.flip()
        clock.tick(60)


def show_ghost(screen, audio_manager):
    clock = pygame.time.Clock()
    audio_manager.stop_all_sounds()
    ghost_images = [load_image(resource_path(f"images/ghost_{i}.png"), scale_factor=1) for i in range(5)]

    Ghost_Scale_Factor = 5
    ghost_images = [
        pygame.transform.scale(image, (image.get_width() * Ghost_Scale_Factor, image.get_height() * Ghost_Scale_Factor))
        for image in ghost_images]

    bg = load_image(resource_path("images/background_ghost.jpg"), scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 200))

    ghost_index = 0
    animation_speed = 100
    last_update = pygame.time.get_ticks()

    ghost_sound = audio_manager.load_sound(resource_path("sounds/ghost_sound.mp3"))
    ghost_sound.play(-1)

    running = True
    while running:
        now = pygame.time.get_ticks()
        screen.blit(bg, (0, 0))

        if now - last_update > animation_speed:
            ghost_index = (ghost_index + 1) % len(ghost_images)
            last_update = now

        ghost_image = ghost_images[ghost_index]
        screen.blit(ghost_image, (WIDTH // 2 - ghost_image.get_width() // 2, HEIGHT // 2 - ghost_image.get_height() // 2))

        draw_text("Дух пустыни остановил вас.", button_font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2 + 180, center=True)
        draw_text("Соберите больше морковок в следующей попытке.", button_font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2 + 220, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                audio_manager.stop_all_sounds()
                quit_game()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                audio_manager.stop_all_sounds()
                main_menu(screen)
                return

        pygame.display.flip()
        clock.tick(60)


def show_game_over_screen(screen):
    clock = pygame.time.Clock()
    bg = load_image(resource_path("images/sky3.jpg"), scale_factor=1)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT + 200))
    while True:
        screen.blit(bg, (0, 0))
        draw_text("GAME OVER", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 3)
        draw_text("Нажмите любую клавишу, чтобы вернуться в меню", button_font, FONT_COLOR, screen, WIDTH // 2,
                  HEIGHT // 2)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                main_menu(screen)  # Вернуться в главное меню
                return

        pygame.display.flip()
        clock.tick(60)



def game_loop(screen, level):
    all_sprites = pygame.sprite.Group()
    carrots_group = pygame.sprite.Group()
    player = Player(WIDTH // 2 - 200, HEIGHT + 40, WIDTH, HEIGHT)
    player.level_number = level
    player.lives = 5
    all_sprites.add(player)

    audio_manager = AudioManager()
    level_data = LEVELS[level]
    music_path = level_data.get("music", "sounds/in_game_music.mp3")
    audio_manager.load_music(resource_path(music_path))
    audio_manager.set_music_volume(SETTINGS['music_volume'])
    audio_manager.play_music(loops=-1)

    jump_sound = audio_manager.load_sound(resource_path("sounds/jump_sound.wav"))
    jump_sound.set_volume(0.1)
    walk_sound = audio_manager.load_sound(resource_path("sounds/walk_sound.wav"))
    demon_death = audio_manager.load_sound(resource_path("sounds/demon_death.mp3"))
    demon_death.set_volume(1.0)
    carrot_sound = audio_manager.load_sound(resource_path("sounds/carrot_pickup.mp3"))
    carrot_sound.set_volume(1.0)
    level_complete_sound = audio_manager.load_sound(resource_path("sounds/level_complete.wav"))
    kick_sound = audio_manager.load_sound(resource_path("sounds/kick_sound.wav"))
    kick_sound.set_volume(0.1)

    bg_path = level_data["background"]
    bg = load_image(resource_path(bg_path), scale_factor=1)
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

    from src.Carrot import Carrot
    for x, y in level_data["carrots"]:
        carrot = Carrot(x, y)
        all_sprites.add(carrot)
        carrots_group.add(carrot)

    enemies_group = pygame.sprite.Group()
    for enemy_data in level_data.get("enemies", []):
        enemy = Enemy(
            enemy_data["x"],
            enemy_data["y"],
            enemy_data.get("move_range", 150),
            enemy_data.get("speed", 2)
        )
        all_sprites.add(enemy)
        enemies_group.add(enemy)

    finish_images = level_data.get("finish_images", [])
    finish_sprite = FinishSprite(*level_data["finish"], finish_images)
    all_sprites.add(finish_sprite)

    # Загрузка босса на уровень 4
    boss_group = pygame.sprite.Group()
    if level == 4 and "boss" in level_data:
        boss_info = level_data["boss"]
        boss = Boss(
            x=boss_info["x"],
            y=boss_info["y"],
            move_range=boss_info.get("move_range", 200),
            speed=boss_info.get("speed", 2),
            health=boss_info.get("health", 20)
        )
        all_sprites.add(boss)
        boss_group.add(boss)



    running = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    carrots_collected = 0

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
                    pause_menu(screen, level)
                    while is_paused:
                        pygame.time.delay(50)
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.x_speed = 0

        # Обновление игрока и врагов
        player.update(platforms, enemies_group, audio_manager, kick_sound)
        enemies_group.update()

        if player.rect.top > HEIGHT + 200:
            player.take_damage()
            if player.lives <= 0:
                audio_manager.stop_all_sounds()
                show_game_over_screen(screen)
                return
            else:
                restart_level(screen, level)
                return

        boss_group.update(player.rect)  # Вызывает handle_ai и animate


                # Сбор морковок
        collected = pygame.sprite.spritecollide(player, carrots_group, True)
        if collected:
            carrots_collected += len(collected)
            global total_carrots_collected
            total_carrots_collected += len(collected)
            audio_manager.play_sound(carrot_sound)

        enemy_collision = pygame.sprite.spritecollide(player, enemies_group, False)
        for enemy in enemy_collision:
            # Проверяем, был ли прыжок сверху (убийство врага)
            if player.y_speed > 0 and player.rect.bottom <= enemy.rect.top + 10:
                enemies_group.remove(enemy)
                enemy.kill()
                player.y_speed = -8
                audio_manager.play_sound(kick_sound)
            else:
                # Столкновение сбоку/снизу — игрок получает урон и отбрасывается
                player.lives -= 1
                if player.lives <= 0:
                    audio_manager.stop_all_sounds()
                    show_game_over_screen(screen)
                    return
                else:
                    # Определяем направление отбрасывания
                    if player.rect.centerx < enemy.rect.centerx:
                        # Игрок слева от врага → отбрасываем влево
                        player.rect.x = max(0, player.rect.x - 150)
                    else:
                        # Игрок справа от врага → отбрасываем вправо
                        player.rect.x = min(WIDTH - player.rect.width, player.rect.x + 150)

                    player.rect.y = player.rect.bottom - player.rect.height
                    player.y_speed = 0
                    player._is_jumping = False

        # Столкновение с боссом (прыжок сверху)
        # Столкновение с боссом
        boss_hits = pygame.sprite.spritecollide(player, boss_group, False)
        for boss in boss_hits:
            # Прыжок сверху — игрок атакует босса
            if player.y_speed > 0 and player.rect.bottom <= boss.rect.top + 10:
                boss.take_damage()
                player.y_speed = -8  # Отскок вверх
                audio_manager.play_sound(kick_sound)
                print(f"HP босса: {boss.health}")

                # Отбрасываем игрока
                if player.rect.centerx < boss.rect.centerx:
                    player.rect.x -= 100  # Влево
                else:
                    player.rect.x += 100  # Вправо

            # Иначе — игрок получает урон от босса
            else:
                if hasattr(boss, 'take_damage'):
                    # Игрок теряет жизнь только один раз за касание
                    # Чтобы не терять жизни каждую секунду, можно использовать глобальную проверку
                    global boss_can_damage
                    if not hasattr(boss, "last_hit_time") or pygame.time.get_ticks() - boss.last_hit_time > 1000:
                        player.take_damage()
                        boss.last_hit_time = pygame.time.get_ticks()

                        # Отбрасываем игрока
                        if player.rect.centerx < boss.rect.centerx:
                            player.rect.x -= 100  # Влево
                        else:
                            player.rect.x += 100  # Вправо

                # Проверка условия завершения уровня
        if level == 4:
            if not boss_group:
                audio_manager.play_sound(demon_death)
                pygame.time.delay(2000)
                audio_manager.stop_all_sounds()
                # Победа над боссом → показываем экран победы
                show_victory(screen, audio_manager)
                return
        else:
            if finish_sprite and pygame.sprite.collide_rect(player, finish_sprite):
                audio_manager.play_sound(level_complete_sound)
                next_level_screen(screen, level + 1,
                                  total_carrots=len(level_data["carrots"]),
                                  carrots_collected=carrots_collected,
                                  time_taken=(pygame.time.get_ticks() - start_time) / 1000)
                running = False  # выходим из текущего цикла
                game_loop(screen, level+1)
                return

        # Отрисовка
        screen.blit(bg, (0, 0))
        draw_text(f"Уровень: {level}", font, FONT_COLOR, screen, 20, 10, center=False)
        draw_text(f"Время: {int((pygame.time.get_ticks() - start_time) / 1000)}", font, FONT_COLOR, screen, 22, 35,
                  center=False)
        draw_text(f"Морковки: {total_carrots_collected}", font, FONT_COLOR, screen, 850, 35, center=False)
        draw_text(f"Жизни игрока: {player.lives}", font, FONT_COLOR, screen, 850, 10, center=False)
        # --- Отображение здоровья босса (только на уровне 4) ---
        if level == 4 and boss_group:
            for boss in boss_group:
                # Выводим здоровье босса
                font_hp = pygame.font.Font(None, 36)
                health_text = font_hp.render(f"Босс HP: {boss.health}", True, (255, 0, 0))  # Красный текст
                screen.blit(health_text, (WIDTH // 2 - 80, 20))
        all_sprites.draw(screen)
        pygame.display.flip()