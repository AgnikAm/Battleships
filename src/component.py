from dataclasses import dataclass
from pygame import Surface, Rect


@dataclass
class Component:
    surface: Surface
    rect: Rect

    def blit(self, background: Surface) -> None:
        background.blit(self.surface, self.rect)
