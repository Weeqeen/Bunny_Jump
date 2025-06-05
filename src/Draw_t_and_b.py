import pygame


pygame.init()
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 102, 204)
BUTTON_HOVER_COLOR = (0, 153, 255)


def draw_text(text, font, color, surface, x, y, center=True):
    text_surface = font.render(text, True, color)  # Создаем текстовое изображение
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (x, y)  # Центрируем текст по заданным координатам
    else:
        text_rect.topleft = (x, y)  # Устанавливаем в левый верхний угол

    surface.blit(text_surface, text_rect)  # Рисуем текст на поверхности


# Draw_t_and_b.py
def draw_button(text, font, surface, x, y, width, height, action=None, hover_color=(0, 200, 0), default_color=(0, 153, 0)):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Проверяем, находится ли курсор внутри кнопки
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        button_color = hover_color
    else:
        button_color = default_color

    # Рисуем кнопку
    pygame.draw.rect(surface, button_color, (x, y, width, height))

    # Рисуем текст на кнопке
    draw_text(text, font, FONT_COLOR, surface, x + width // 2, y + height // 2)

    # Выполняем действие при нажатии
    if button_color == hover_color and mouse_click[0]:
        print(f"Кнопка '{text}' нажата")  # ← Добавляем этот вывод
        if action:
            action()