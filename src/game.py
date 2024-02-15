import pygame
from pygame import Surface, Rect

class GameScreen:
    surface: Surface

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

    def draw(self) -> None:
        pass
