import pygame
from pygame import Surface, Rect


class MenuScreen:
    surface: Surface
    start: Rect
    quit: Rect

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

        width, height = surface.get_size()

        self.start = draw_text(
            surface,  # funkcję trzeba napisać tak, żeby nie zmieniała stanu ekranu tylko zwracała obiekt
            "Start", 
            None, 
            70, 
            (101, 88, 130), 
            width // 2, 
            height // 3 + 100
        )

        self.quit = draw_text(
            surface, 
            "Quit", 
            None, 
            70, 
            (101, 88, 130), 
            width // 2, 
            height // 3 + 200
        )

    def draw(self) -> None:
        # tu wywołać surface.blit()
        pass
