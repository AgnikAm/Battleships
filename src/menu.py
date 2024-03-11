import pygame
from pygame import Surface, Rect, image

from component import Component
from drawing import draw_text
from drawing import WHITE, MENU_BACKGROUND, MENU_BOX, MENU_PLATE, MENU_PLATE_HIGHLIGHT, ALKHEMIKAL


class MenuScreen:
    surface: Surface

    background: Surface
    title: Component

    start: Component
    rules: Component
    quit: Component

    start_rect: Rect
    rules_rect: Rect
    quit_rect: Rect

    textbox_image: Surface
    textbox_rect: Rect

    menu_plate_image: Surface
    menu_plate_rect: Rect
    menu_plate_highlight_image:Surface

    highlight: str


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
            WHITE, 
            (width * 0.27, height // 8)
        )

        self.start = draw_text(
            "Start", 
            ALKHEMIKAL, 
            int(height * 0.08), 
            WHITE, 
            (490, 300)
        )

        self.rules = draw_text(
            "Rules", 
            ALKHEMIKAL, 
            int(height * 0.08), 
            WHITE, 
            (490, 450)
        )

        self.quit = draw_text(
            "Quit", 
            ALKHEMIKAL, 
            int(height * 0.08), 
            WHITE, 
            (490, 600)
        )

        self.start_rect = Rect(
            350,
            290,
            280,
            90
        )

        self.rules_rect = Rect(
            350,
            440,
            280,
            90
        )

        self.quit_rect = Rect(
            350,
            590,
            280,
            90
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

        self.menu_plate_highlight_image = pygame.transform.scale(
            image.load(MENU_PLATE_HIGHLIGHT),
            (375, 190)
        )

        self.highlight = "None"


    def draw_highlight(self, coords: tuple[int, int]) -> None:
        self.surface.blit(self.menu_plate_highlight_image, coords)


    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        if self.highlight == "start":
            self.surface.blit(self.menu_plate_highlight_image, (303, 230))
        else:
            self.surface.blit(self.menu_plate_image, (340, 230))

        if self.highlight == "rules":
            self.surface.blit(self.menu_plate_highlight_image, (303, 380))
        else:
            self.surface.blit(self.menu_plate_image, (340, 380))

        if self.highlight == "quit":
            self.surface.blit(self.menu_plate_highlight_image, (303, 530))
        else:
            self.surface.blit(self.menu_plate_image, (340, 530))

        self.surface.blit(self.textbox_image, self.textbox_rect)

        self.start.blit(self.surface)
        self.rules.blit(self.surface)
        self.quit.blit(self.surface)
