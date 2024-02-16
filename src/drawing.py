import pygame
from pygame import Surface, Rect
from typing import Optional
from component import Component

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