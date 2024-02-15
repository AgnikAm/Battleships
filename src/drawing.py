import pygame
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