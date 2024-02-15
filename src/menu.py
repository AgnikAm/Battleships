import pygame
from pygame import Surface, Rect

from component import Component
from drawing import draw_text

BACKGROUND = 'assets\menu_bg.jpg'


class MenuScreen:
    surface: Surface

    background: Surface
    start: Component
    quit: Component


    def __init__(self, surface: Surface) -> None:
        self.surface = surface

        width, height = surface.get_size()

        self.start = draw_text(
            "Start", 
            None, 
            height // 12, 
            (101, 88, 130), 
            (width // 2, height // 3)
        )

        self.quit = draw_text(
            "Quit", 
            None, 
            height // 12, 
            (101, 88, 130), 
            (width // 2, height // 3 + int(height / 10))
        )

        self.background = pygame.transform.scale(
            pygame.image.load(BACKGROUND), 
            surface.get_size()
        )

    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        self.start.blit(self.surface)
        self.quit.blit(self.surface)
