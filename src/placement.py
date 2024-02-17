import pygame
from pygame import Surface, Rect, draw, image
from typing import Optional

from component import Component
from grid import Grid
from gameboard import GameBoard
from ship import Ship
from drawing import draw_text
from drawing import WHITE, LIGHT_BROWN, DARK_BROWN, PINK

BACKGROUND = 'assets\game_bg.jpg'
MENU_ICON = 'assets\home-icon.png'
ACCEPT_ICON = 'assets\check-icon.png'


class PlacementScreen:
    surface: Surface
    background: Surface
    width: int
    height: int

    bar: Rect
    header: Component

    menu: Rect
    menu_icon: Surface
    menu_icon_rect: Rect

    accept: Rect
    accept_icon: Surface
    menu_icon_rect: Rect

    grid: Grid

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

        self.width, self.height = surface.get_size()

        self.background = pygame.transform.scale(
            pygame.image.load(BACKGROUND), 
            surface.get_size()
        )


        self.bar = Rect(
            self.surface.get_rect().centerx - (self.height * 0.75 - self.height * 0.75 // 10) // 2,
            0,
            self.height * 0.75,
            self.height * 0.1
        )


        self.header = draw_text(
            "Prepare for battle",
            None,
            self.height // 15,
            WHITE,
            (self.bar.centerx, self.bar.height // 5)
        )


        self.menu = Rect(
            0,
            self.height - self.width // 10,
            self.width // 10,
            self.width // 10
        )


        self.menu_icon = pygame.transform.scale(
            image.load(MENU_ICON),
            (self.width * 0.05, self.width * 0.05)
        )


        self.menu_icon_rect = self.menu_icon.get_rect(
            center = (self.menu.centerx - self.width * 0.015, self.menu.centery + self.height * 0.02)
        )


        self.accept = Rect(
            self.width - self.width // 10,
            self.height - self.width // 10,
            self.width // 10,
            self.width // 10
        )


        self.accept_icon = pygame.transform.scale(
            image.load(ACCEPT_ICON),
            (self.width * 0.05, self.width * 0.05)
        )


        self.accept_icon_rect = self.menu_icon.get_rect(
            center = (self.accept.centerx + self.width * 0.015, self.accept.centery + self.height * 0.02)
        )


        self.grid = Grid(
            self.surface,
            (self.height * 0.75, self.height * 0.75),
            10,
            10,
            (self.surface.get_rect().centerx - (self.height * 0.75 - self.height * 0.75 // 10) // 2, self.height // 5),
            self.height * 0.75 // 10,
            DARK_BROWN,
            LIGHT_BROWN
        )
        
        
    def place_ship(self, position: tuple[int, int]) -> None:
        self.grid.occupied[position] = True

        # grid[position] = coś  # nowy wygląd kwadratu na pozycji


    def collide_field(self, position: tuple[int, int]) -> Optional[tuple[int, int]]:
        for pos, component in self.grid.cells.items():
            if component.rect.collidepoint(position):
                return pos


    def draw(self) -> None:

        self.surface.blit(self.background, (0, 0))
        
        draw.rect(self.surface, DARK_BROWN, self.bar)
        self.header.blit(self.surface)

        draw.circle(self.surface, DARK_BROWN, self.menu.bottomleft, self.width // 10)
        self.surface.blit(self.menu_icon, self.menu_icon_rect)

        draw.circle(self.surface, DARK_BROWN, self.accept.bottomright, self.width // 10)
        self.surface.blit(self.accept_icon, self.accept_icon_rect)

        self.grid.draw()
        
