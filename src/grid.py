import pygame
from pygame import Surface, Rect
from component import Component
from typing import Optional


def draw_full_rect(
        size: tuple[int, int], 
        color: tuple[int, int, int], 
        midtop: tuple[int, int]
) -> Component:
    rect = Rect(*midtop, *size)
    surface = Surface(size)
    surface.fill(color)

    return Component(surface, rect)


class Grid:
    surface: Surface
    size: tuple[int, int]
    background: Component
    cells: dict[tuple[int, int], Component]

    highlighted: Optional[tuple[int, int]]

    cell_size: tuple[int, int]
    cell_color: tuple[int, int, int]
    highlighted_color: tuple[int, int, int]

    def __init__(
            self, 
            surface: Surface,
            size: tuple[int, int], 
            color: tuple[int, int, int],
            midtop: tuple[int, int],
            cell_size: tuple[int, int], 
            cell_color: tuple[int, int, int],
            highlighted_color: tuple[int, int, int]
    ) -> None:
        self.surface = surface
        width, height = size        
        self.background = draw_full_rect(size, color, midtop)

        self.cells = dict(
            ((row, col), draw_full_rect(cell_size, cell_color, (row, col)))
            for row in range(width)
            for col in range(height)
        )

        self.highlighted = None
        self.cell_size = cell_size
        self.cell_color = cell_color
        self.highlighted_color = highlighted_color

    def highlight(self, cell: tuple[int, int]) -> None:
        self.cells[cell] = draw_full_rect(
            self.cell_size, 
            self.highlighted_color, 
            cell
        )

        if self.highlighted is not None:
            self.cells[self.highlight] = draw_full_rect(
            self.cell_size, 
            self.cell_color, 
            self.highlighted
        )
        
        self.highlighted = cell

    def draw(self) -> None:
        self.background.blit(self.surface)
        
        for field in self.cells.values():
            field.blit(self.background.surface)