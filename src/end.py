import pygame
from pygame import Surface, Rect, draw, image

from component import Component
from gameboard import GameBoard
from drawing import draw_text
from drawing import WHITE, DARK_BROWN, GAME_BACKGROUND, MENU_ICON


class EndScreen:
    surface: Surface
    background: Surface
    width: int
    height: int

    player_score: int
    enemy_score: int

    bar: Rect
    header: Component
    player_score_text: Component
    enemy_score_text: Component

    menu: Rect
    menu_icon: Surface
    menu_icon_rect: Rect

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

        self.width, self.height = surface.get_size()

        self.background = pygame.transform.scale(
            pygame.image.load(GAME_BACKGROUND), 
            surface.get_size()
        )

        self.bar = Rect(
            self.surface.get_rect().centerx - self.height // 2,
            self.surface.get_rect().centery - self.height * 0.75 // 2,
            self.height,
            self.height * 0.75
        )

        self.menu = Rect(
            self.width - self.width // 12,
            self.height - self.width // 12,
            self.width // 12,
            self.width // 12
        )

        self.menu_icon = pygame.transform.scale(
            image.load(MENU_ICON),
            (self.width * 0.04, self.width * 0.04)
        )

        self.menu_icon_rect = self.menu_icon.get_rect(
            center = (self.menu.centerx + self.width * 0.015, self.menu.centery + self.height * 0.02)
        )


    def get_scores(self, player: GameBoard, enemy: GameBoard) -> None:
        self.player_score = player.score
        self.enemy_score = enemy.score
    

    def set_header(self):
        if self.player_score > self.enemy_score:
            self.header = draw_text(
                'Winner: player',
                None,
                self.height // 10,
                WHITE,
                (self.bar.centerx, self.bar.centery - self.height // 10)
            )

        elif self.player_score < self.enemy_score:
            self.header = draw_text(
                'Winner: enemy',
                None,
                self.height // 10,
                WHITE,
                (self.bar.centerx, self.bar.centery - self.height // 10)
            )
        
        else:
            self.header = draw_text(
                'Draw',
                None,
                self.height // 10,
                WHITE,
                (self.bar.centerx, self.bar.centery - self.height // 10)
            )

        
    def set_player_scores(self) -> None:
        self.player_score_text = draw_text(
            f"Player's score: {self.player_score}",
            None,
            self.height // 12,
            WHITE,
            (self.bar.centerx, self.bar.centery)
        )

    
    def set_enemy_scores(self) -> None:
        self.enemy_score_text = draw_text(
            f"Enemy's score {self.enemy_score}",
            None,
            self.height // 12,
            WHITE,
            (self.bar.centerx, self.bar.centery + self.height // 12)
        )


    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        draw.rect(self.surface, DARK_BROWN, self.bar)
        self.header.blit(self.surface)
        self.player_score_text.blit(self.surface)
        self.enemy_score_text.blit(self.surface)

        draw.circle(self.surface, DARK_BROWN, self.menu.bottomright, self.width // 12)
        self.surface.blit(self.menu_icon, self.menu_icon_rect)