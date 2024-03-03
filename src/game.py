import pygame
from pygame import Surface, Rect, draw, image
from typing import Optional

from component import Component
from grid import Grid
from gameboard import GameBoard
from drawing import draw_text
from drawing import WHITE, DARK_BROWN, LIGHT_BROWN, YELLOW, GAME_BACKGROUND, MENU_ICON


class GameScreen:
    surface: Surface
    background: Surface
    width: int
    height: int

    bar: Rect
    header: Component

    menu: Rect
    menu_icon: Surface
    menu_icon_rect: Rect

    grid_player: Grid
    grid_enemy: Grid

    def __init__(self, surface: Surface, occupied: dict[tuple[int, int]]) -> None:
        self.surface = surface

        self.width, self.height = surface.get_size()

        self.background = self.background = pygame.transform.scale(
            pygame.image.load(GAME_BACKGROUND), 
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
            self.height - self.width // 12,
            self.width // 12,
            self.width // 12
        )

        self.menu_icon = pygame.transform.scale(
            image.load(MENU_ICON),
            (self.width * 0.04, self.width * 0.04)
        )

        self.menu_icon_rect = self.menu_icon.get_rect(
            center = (self.menu.centerx - self.width * 0.015, self.menu.centery + self.height * 0.02)
        )

        self.grid_player = Grid(
            self.surface,
            10,
            10,
            (self.surface.get_rect().centerx + self.height * 0.2, self.height // 3),
            self.height * 0.60 // 10,
            DARK_BROWN,
            LIGHT_BROWN
        )
        self.grid_player.occupied = occupied

        self.grid_enemy = Grid(
            self.surface,
            10,
            10,
            (self.menu_icon_rect.right + self.height * 0.2, self.height // 3),
            self.height * 0.60 // 10,
            DARK_BROWN,
            YELLOW
        )


    def collide_field(self, position: tuple[int, int]) -> Optional[tuple[int, int]]:
        for pos, component in self.grid_enemy.cells.items():
            if component.rect.collidepoint(position):
                return pos
            

    def update_ships(self, grid: Grid, board: GameBoard) -> None:
        for ship in board.content.values():
            for segment_coordinates, segment in ship.segments.items():
                if segment.visible:
                    grid.occupied[segment_coordinates] = True


    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        draw.rect(self.surface, DARK_BROWN, self.bar)
        self.header.blit(self.surface)

        draw.circle(self.surface, DARK_BROWN, self.menu.bottomleft, self.width // 12)
        self.surface.blit(self.menu_icon, self.menu_icon_rect)

        self.grid_player.draw()
        self.grid_enemy.draw()
