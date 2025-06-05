import pygame


FONT_COLOR = (255, 255, 255)
BUTTON_DEFAULT_COLOR = (0, 153, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)


def draw_text(text, font, color, surface, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def draw_button(text, font, surface, x, y, width, height, action=None,
                hover_color=(0, 200, 0), default_color=(0, 153, 0)):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    hovered = x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height
    button_color = hover_color if hovered else default_color

    pygame.draw.rect(surface, button_color, (x, y, width, height))
    draw_text(text, font, FONT_COLOR, surface, x + width // 2, y + height // 2)

    if hovered and mouse_click[0]:
        if action:
            action()
        return True
    return False


def draw_slider(x, y, width, height, value, surface):
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height))
    slider_x = x + int(value * width)
    pygame.draw.circle(surface, (255, 255, 255), (slider_x, y + height // 2), 10)


def check_slider(x, y, width, height, mouse_pos):
    return x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height