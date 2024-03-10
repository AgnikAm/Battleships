import pygame
from pygame import Surface, Rect, draw, image
from typing import Optional

from component import Component
from grid import Grid
from drawing import draw_text
from drawing import WHITE, DARK_BROWN, LIGHT_BROWN, GAME_BACKGROUND, MENU_ICON, ACCEPT_ICON, RETRY_ICON, TEXT_BOX, PLACEMENT_PLATE

class PlacementScreen:
    surface: Surface
    width: int
    height: int
    background: Surface

    bar: Rect
    bar_image: Surface
    bar_image_rect: Rect
    header: Component

    menu_icon: Surface
    menu_icon_rect: Rect

    accept_icon: Surface
    accept_icon_rect: Rect

    auto_place: Rect
    auto_place_text: Component

    plate_image: Surface
    plate_rect: Rect

    retry_icon: Surface
    retry_icon_rect: Rect

    grid: Grid

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

        self.width, self.height = surface.get_size()

        self.background = pygame.transform.scale(
            pygame.image.load(GAME_BACKGROUND), 
            surface.get_size()
        )

        self.bar = Rect(
            self.surface.get_rect().centerx - (self.height * 0.75 - self.height * 0.75 // 10) // 2,
            0,
            self.height * 0.75,
            self.height * 0.1
        )

        self.bar_image = pygame.transform.scale(
            image.load(TEXT_BOX),
            (self.width * 0.40, self.width * 0.06)
        )

        self.bar_image_rect = self.bar_image.get_rect(
            center = (self.bar.centerx, self.bar.centery + self.height * 0.02)
        )

        self.header = draw_text(
            '',
            None,
            self.height // 15,
            WHITE,
            (self.bar.centerx, self.bar.height * 0.6)
        )

        self.menu_icon = pygame.transform.scale(
            image.load(MENU_ICON),
            (self.width * 0.06, self.width * 0.06)
        )

        self.menu_icon_rect = self.menu_icon.get_rect(
            center = (80, 940)
        )

        self.accept_icon = pygame.transform.scale(
            image.load(ACCEPT_ICON),
            (self.width * 0.06, self.width * 0.06)
        )

        self.accept_icon_rect = self.menu_icon.get_rect(
            center = (1840, 940)
        )

        self.auto_place = Rect(
            self.width * 0.80,
            self.height // 2 - self.height * 0.2,
            self.width // 8,
            self.height // 12
        )

        self.auto_place_text = draw_text(
            'Auto place',
            None,
            self.height // 18,
            WHITE,
            (self.auto_place.centerx, self.auto_place.centery - self.height // 50)
        )

        self.plate_image = pygame.transform.scale(
            image.load(PLACEMENT_PLATE),
            (240, 90)
        )

        self.plate_rect = self.plate_image.get_rect(
            center = self.auto_place_text.rect.center
        )

        self.retry_icon = pygame.transform.scale(
            image.load(RETRY_ICON),
            (self.width * 0.06, self.width * 0.06)
        )

        self.retry_icon_rect = self.retry_icon.get_rect(
            center = (self.auto_place_text.rect.centerx, self.auto_place_text.rect.centery + 150)
        )

        self.grid = Grid(
            self.surface,
            10,
            10,
            (self.surface.get_rect().centerx - (self.height * 0.75 - self.height * 0.75 // 10) // 2, self.height * 0.22),
            self.height * 0.75 // 10,
            DARK_BROWN,
            LIGHT_BROWN
        )
        
        
    def place_ship(self, position: tuple[int, int]) -> None:
        self.grid.occupied[position] = True


    def collide_field(self, position: tuple[int, int]) -> Optional[tuple[int, int]]:
        for pos, component in self.grid.cells.items():
            if component.rect.collidepoint(position):
                return pos
            

    def set_header(self, length: Optional[int]) -> None:
        if length:
            self.header = draw_text(
                f'Place ship of size {length}',
                None,
                self.height // 15,
                WHITE,
                (self.bar.centerx, self.bar.height * 0.6)
            )
        else:
            self.header = draw_text(
                'All ships are placed',
                None,
                self.height // 15,
                WHITE,
                (self.bar.centerx, self.bar.height * 0.6)
            )


    def draw(self) -> None:

        self.surface.blit(self.background, (0, 0))
        
        self.surface.blit(self.bar_image, self.bar_image_rect)
        self.header.blit(self.surface)

        self.surface.blit(self.menu_icon, self.menu_icon_rect)
        self.surface.blit(self.accept_icon, self.accept_icon_rect)

        self.surface.blit(self.plate_image, self.plate_rect)
        self.auto_place_text.blit(self.surface)
        self.surface.blit(self.retry_icon, self.retry_icon_rect)

        self.grid.draw()
        
