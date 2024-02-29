import pygame
from pygame import Surface, Rect

from component import Component
from drawing import draw_text
from drawing import LIGHT_PURPLE, MENU_BACKGROUND


class MenuScreen:
    surface: Surface

    background: Surface
    title: Component
    start: Component
    quit: Component


    def __init__(self, surface: Surface) -> None:

        self.surface = surface
        self.background = pygame.transform.scale(
            pygame.image.load(MENU_BACKGROUND), 
            surface.get_size()
        )

        width, height = surface.get_size()

        self.title = draw_text(
            "Battleships", 
            None, 
            int(height * 0.13), 
            LIGHT_PURPLE, 
            (width // 2, height // 4)
        )

        self.start = draw_text(
            "Start", 
            None, 
            int(height * 0.08), 
            LIGHT_PURPLE, 
            (width // 2, height // 3 + 100)
        )

        self.quit = draw_text(
            "Quit", 
            None, 
            int(height * 0.08), 
            LIGHT_PURPLE, 
            (width // 2, height // 3 + 200)
        )


    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        self.title.blit(self.surface)
        self.start.blit(self.surface)
        self.quit.blit(self.surface)
