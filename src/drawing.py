import pygame
from pygame import Surface, Rect
from typing import Optional
from component import Component

WHITE = (255, 255, 255)
CHATHAMS_BLUE = (35, 87, 107)
LIGHT_BROWN = (148, 124, 112)
DARK_BROWN = (82, 53, 38)
PINK = (142, 70, 156)
LIGHT_PURPLE = (101, 88, 130)

def draw_text(
        text: str, 
        font: Optional[str], 
        size: int, 
        color: tuple[int, int, int], 
        midtop: tuple[int, int]
) -> Component:
    surface = pygame.font\
        .Font(font, size)\
        .render(text, 1, color)

    rect = surface.get_rect()
    rect.midtop = midtop

    return Component(surface, rect)

def draw_full_rect(
        size: int, 
        color: tuple[int, int, int],
        upperleft: tuple[int, int],
        position: tuple[int, int]
) -> Component:
    
    left = upperleft[0] + position[0] * size
    top = upperleft[1] + position[1] * size
    surface = Surface((size, size))
    rect = Rect(left, top, size, size)
    surface.fill(color)

    return Component(surface, rect)