import pygame
from pygame import Surface, Rect, draw, image
from typing import Optional

from component import Component
from grid import Grid
from gameboard import GameBoard
from drawing import draw_text
from drawing import WHITE, DARK_BROWN, LIGHT_BROWN, YELLOW, GAME_BACKGROUND, MENU_ICON, TEXT_BOX


class GameScreen:
    surface: Surface
    width: int
    height: int
    background: Surface

    menu_icon: Surface
    menu_icon_rect: Rect

    bar_player: Rect
    bar_enemy: Rect
    bar_image: Surface

    grid_player: Grid
    grid_enemy: Grid

    def __init__(self, surface: Surface, occupied: dict[tuple[int, int]]) -> None:
        self.surface = surface

        self.width, self.height = surface.get_size()

        self.background = self.background = pygame.transform.scale(
            pygame.image.load(GAME_BACKGROUND), 
            surface.get_size()
        )

        self.menu_icon = pygame.transform.scale(
            image.load(MENU_ICON),
            (self.width * 0.06, self.width * 0.06)
        )

        self.menu_icon_rect = self.menu_icon.get_rect(
            center = (80, 940)
        )

        self.bar_player = Rect(
            self.surface.get_rect().centerx + 180,
            self.height * 0.1,
            self.height * 0.66,
            self.height * 0.1
        )

        self.bar_enemy = Rect(
            self.menu_icon_rect.right + 180,
            self.height * 0.1,
            self.height * 0.66,
            self.height * 0.1
        )

        self.bar_image = pygame.transform.scale(
            image.load(TEXT_BOX),
            (self.width * 0.3, self.width * 0.05)
        )

        self.player_text = draw_text(
            'Player',
            None,
            self.height // 15,
            WHITE,
            (self.bar_player.centerx, self.bar_player.centery - self.bar_player.height * 0.1)
        )

        self.enemy_text = draw_text(
            'Enemy',
            None,
            self.height // 15,
            WHITE,
            (self.bar_enemy.centerx, self.bar_enemy.centery - self.bar_enemy.height * 0.1)
        )

        self.grid_player = Grid(
            self.surface,
            10,
            10,
            (self.surface.get_rect().centerx + self.height * 0.2, self.height * 0.3),
            self.height * 0.60 // 10,
            DARK_BROWN,
            LIGHT_BROWN
        )
        
        self.grid_player.occupied = occupied

        self.grid_enemy = Grid(
            self.surface,
            10,
            10,
            (self.menu_icon_rect.right + self.height * 0.2, self.height * 0.3),
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


    def set_enemy_text(self, text: str) -> None:
        self.enemy_text = draw_text(
            f'{text}',
            None,
            self.height // 15,
            WHITE,
            (self.bar_enemy.centerx, self.bar_enemy.centery - self.bar_enemy.height * 0.1)
        )

    
    def set_player_text(self, text: str) -> None:
        self.player_text = draw_text(
            f'{text}',
            None,
            self.height // 15,
            WHITE,
            (self.bar_player.centerx, self.bar_player.centery - self.bar_player.height * 0.1)
        )


    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        self.surface.blit(self.bar_image, 
                          self.bar_image.get_rect(
                            center = (
                                self.bar_player.centerx,
                                  self.bar_player.centery
                                )
                            )
                        )
        
        self.surface.blit(self.bar_image, 
                          self.bar_image.get_rect(
                            center = (
                                self.bar_enemy.centerx,
                                  self.bar_enemy.centery
                                )
                            )
                        )
        
        self.enemy_text.blit(self.surface)
        self.player_text.blit(self.surface)

        self.surface.blit(self.menu_icon, self.menu_icon_rect)

        self.grid_player.draw()
        self.grid_enemy.draw()
