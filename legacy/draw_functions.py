import pygame

def draw_text(screen, text, font_name, font_size, color, x, y):

    f = pygame.font.Font(font_name, font_size)
    text_surface = f.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

    return text_rect