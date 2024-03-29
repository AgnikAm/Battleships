import pygame
import os
from pygame import Surface, Rect
from typing import Optional
from component import Component

MENU_BACKGROUND = os.path.join('../assets', 'menu_bg.png')
GAME_BACKGROUND = os.path.join('../assets', 'game_bg.png')
MENU_ICON = os.path.join('../assets', 'home-icon.png')
ACCEPT_ICON = os.path.join('../assets', 'check-icon.png')
RETRY_ICON = os.path.join('../assets', 'retry-icon.png')
TEXT_BOX = os.path.join('../assets', 'text_box.png')
TEXT_BOX_BIG = os.path.join('../assets', 'text_box_big.png')
MENU_BOX = os.path.join('../assets', 'menu_box1.png')
MENU_PLATE = os.path.join('../assets', 'menu_plate.png')
MENU_PLATE_HIGHLIGHT = os.path.join('../assets', 'menu_plate_highlight.png')
PLACEMENT_PLATE = os.path.join('../assets', 'placement_plate.png')
FORWARD_ICON = os.path.join('../assets', 'forward-icon.png')

WHITE = (255, 255, 255)
DARK_BROWN = (82, 53, 38)
LIGHT_BROWN = (148, 124, 112)
CHATHAMS_BLUE = (35, 87, 107)
YELLOW = (209, 171, 67)
RED = (133, 52, 52)
LIGHT_BLUE = (71, 144, 168)

ALKHEMIKAL = os.path.join('../assets', 'Alkhemikal.ttf')


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