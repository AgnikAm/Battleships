import pygame
from pygame import Surface, Rect, draw, image

from component import Component
from gameboard import GameBoard
from drawing import draw_text
from drawing import DARK_BROWN, GAME_BACKGROUND, MENU_ICON, TEXT_BOX_BIG, ALKHEMIKAL


class EndScreen:
    surface: Surface
    width: int
    height: int
    background: Surface

    bar: Rect
    bar_image: Surface
    bar_image_rect: Rect

    menu: Rect
    menu_icon: Surface
    menu_icon_rect: Rect

    header: Component
    player_score: int
    enemy_score: int
    player_score_text: Component
    enemy_score_text: Component

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

        self.bar_image = pygame.transform.scale(
            image.load(TEXT_BOX_BIG),
            (self.width // 2, self.width // 3)
        )

        self.bar_image_rect = self.bar_image.get_rect(
            center = self.bar.center
        )

        self.menu = Rect(
            self.width - self.width // 12,
            self.height - self.width // 12,
            self.width // 12,
            self.width // 12
        )

        self.menu_icon = pygame.transform.scale(
            image.load(MENU_ICON),
            (self.width * 0.06, self.width * 0.06)
        )

        self.menu_icon_rect = self.menu_icon.get_rect(
            center = (1840, 940)
        )


    def get_scores(self, player: GameBoard, enemy: GameBoard) -> None:
        self.player_score = player.score
        self.enemy_score = enemy.score
    

    def set_header(self):
        if self.player_score > self.enemy_score:
            self.header = draw_text(
                "Congratulations, Captain!",
                ALKHEMIKAL,
                self.height // 14,
                DARK_BROWN,
                (self.bar.centerx, self.bar.centery - self.height // 10)
            )

        elif self.player_score < self.enemy_score:
            self.header = draw_text(
                "Ye be walkin' the plank this time, matey!",
                ALKHEMIKAL,
                self.height // 20,
                DARK_BROWN,
                (self.bar.centerx, self.bar.centery - self.height // 10)
            )
        
        else:
            self.header = draw_text(
                'Arrr! The sea is undecided today',
                ALKHEMIKAL,
                self.height // 16,
                DARK_BROWN,
                (self.bar.centerx, self.bar.centery - self.height // 10)
            )

        
    def set_player_scores(self) -> None:
        self.player_score_text = draw_text(
            f"Player's score: {self.player_score}",
            ALKHEMIKAL,
            self.height // 12,
            DARK_BROWN,
            (self.bar.centerx, self.bar.centery)
        )

    
    def set_enemy_scores(self) -> None:
        self.enemy_score_text = draw_text(
            f"Enemy's score {self.enemy_score}",
            ALKHEMIKAL,
            self.height // 12,
            DARK_BROWN,
            (self.bar.centerx, self.bar.centery + self.height // 12)
        )


    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        self.surface.blit(self.bar_image, self.bar_image_rect)

        self.header.blit(self.surface)
        self.player_score_text.blit(self.surface)
        self.enemy_score_text.blit(self.surface)

        self.surface.blit(self.menu_icon, self.menu_icon_rect)
