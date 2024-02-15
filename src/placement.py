import pygame
from pygame import Surface, Rect, draw
from typing import Optional

from component import Component
from drawing import draw_text
from grid import Grid

BACKGROUND = 'assets\game_bg.jpg'

class PlacementScreen:
    surface: Surface
    width: int
    height: int
    
    menu: Rect
    accept: Rect
    grid: dict[tuple[int, int], Component]

    background: Surface
    header: Component
    board: Grid

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

        self.width, self.height = surface.get_size()

        self.background = pygame.transform.scale(
            pygame.image.load(BACKGROUND), 
            surface.get_size()
        )

        self.header = draw_text(
            "Prepare for battle",
            None,
            self.height // 15,
            (255, 255, 255),
            (self.width // 2, self.height // 80)
        )

        self.menu = Rect(
            0,
            self.height - self.width // 8,
            self.width // 8,
            self.width // 8
        )

        self.accept = Rect(
            self.width - self.width // 8,
            self.height - self.width // 8,
            self.width // 8,
            self.width // 8
        )

        self.board = Grid(
            self.surface,
            (self.width // 2, self.width // 2),
            (255, 255, 255),
            (self.width // 4, self.height // 6),
            (10, 10),
            (80, 181, 152),
            (101, 88, 130)
        )
        
    def place_ship(self, position: tuple[int, int]) -> None:
        # grid[position] = coś  # nowy wygląd kwadratu na pozycji
        pass

    def collide_field(self, position: tuple[int, int]) -> Optional[tuple[int, int]]:
        for pos, component in self.grid.items():
            if component.rect.collidepont(position):
                return pos

    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))
        
        self.header.blit(self.surface)
        draw.circle(self.surface, (94, 68, 46), self.menu.bottomleft, self.width // 10)
        draw.circle(self.surface, (94, 68, 46), self.accept.bottomright, self.width // 10)
        self.board.draw()
        
