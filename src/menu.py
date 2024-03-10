import pygame
from pygame import Surface, Rect, image

from component import Component
from drawing import draw_text
from drawing import LIGHT_PURPLE, MENU_BACKGROUND, MENU_BOX, MENU_PLATE


class MenuScreen:
    surface: Surface

    background: Surface
    title: Component

    start: Component
    rules: Component
    quit: Component

    textbox_image: Surface
    textbox_rect: Rect

    menu_plate_image: Surface
    menu_plate_rect: Rect


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
            (width // 4, height // 8)
        )

        self.start = draw_text(
            "Start", 
            None, 
            int(height * 0.08), 
            LIGHT_PURPLE, 
            (485, 310)
        )

        self.rules = draw_text(
            "Rules", 
            None, 
            int(height * 0.08), 
            LIGHT_PURPLE, 
            (485, 460)
        )

        self.quit = draw_text(
            "Quit", 
            None, 
            int(height * 0.08), 
            LIGHT_PURPLE, 
            (485, 610)
        )

        self.textbox_image = pygame.transform.scale(
            image.load(MENU_BOX),
            (800, 200)
        )

        self.textbox_rect = self.textbox_image.get_rect(
            center = (self.title.rect.centerx, self.title.rect.centery)
        )

        self.menu_plate_image = pygame.transform.scale(
            image.load(MENU_PLATE),
            (300, 150)
        )


    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        self.surface.blit(self.menu_plate_image, (340, 230))
        self.surface.blit(self.menu_plate_image, (340, 380))
        self.surface.blit(self.menu_plate_image, (340, 530))
        self.surface.blit(self.textbox_image, self.textbox_rect)

        self.title.blit(self.surface)
        self.start.blit(self.surface)
        self.rules.blit(self.surface)
        self.quit.blit(self.surface)
