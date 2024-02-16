import pygame
from pygame import Surface, Rect, draw
from component import Component
from typing import Optional

from drawing import draw_text, draw_full_rect

class Grid:
    surface: Surface
    size: tuple[int, int]
    upperleft: tuple[int, int]
    cell_size: int
    cell_color: tuple[int, int, int]
    highlighted_color: tuple[int, int, int]

    cells: dict[tuple[int, int], Component]
    axis_x: Rect
    axis_y: Rect

    highlighted: Optional[tuple[int, int]]


    def __init__(
            self, 
            surface: Surface,
            size: tuple[int, int], 
            upperleft: tuple[int, int],
            cell_size: int, 
            cell_color: tuple[int, int, int],
            highlighted_color: tuple[int, int, int]
    ) -> None:
        
        self.surface = surface
        self.size = size
        self.upperleft = upperleft
        self.cell_size = cell_size
        self.cell_color = cell_color
        self.highlighted_color = highlighted_color


        self.cells = dict(
            ((row, col), draw_full_rect(cell_size, cell_color, upperleft, (row, col)))
            for row in range(10)
            for col in range(10)
        )

        self.axis_y = Rect(
            upperleft[0] - cell_size,
            upperleft[1],
            cell_size,
            cell_size * 10
        )

        self.axis_x = Rect(
            upperleft[0],
            upperleft[1] - cell_size,
            cell_size * 10,
            cell_size
        )

        self.highlighted = None
        

    def highlight(self, cell: tuple[int, int]) -> None:

        self.cells[cell] = draw_full_rect(
            self.cell_size, 
            self.highlighted_color,
            self.upperleft, 
            cell
        )

        '''if self.highlighted is not None:
            self.cells[self.highlight] = draw_full_rect(
            self.cell_size, 
            self.cell_color,
            self.upperleft,
            self.highlighted
        )'''
        
        self.highlighted = cell

    def assign_axis_x(self, col) -> Component:

        letter_text = chr(ord('A') + col)
        return draw_text(letter_text,
                         None,
                         int(self.size[1] * 0.08),
                         (255, 255, 255),
                         (self.axis_x.x + col * self.cell_size + self.cell_size // 2,
                         self.axis_x.y + self.cell_size // 4)
                        )
    
    def assign_axis_y(self, row) -> Component:

        number_text = str(row + 1)
        return draw_text(number_text,
                         None,
                         int(self.size[1] * 0.08),
                         (255, 255, 255),
                         (self.axis_y.x + self.cell_size // 2,
                         self.axis_y.y + row * self.cell_size + self.cell_size // 4)
                        )


    def draw(self) -> None:

        draw.rect(self.surface, (35, 87, 107), self.axis_x)
        draw.rect(self.surface, (35, 87, 107), self.axis_y)

        for i in range(10):
            self.assign_axis_y(i).blit(self.surface)
            self.assign_axis_x(i).blit(self.surface)

        for cell in self.cells.values():
            draw.rect(self.surface,
                      (255, 255, 255),
                      cell.rect,
                      1
                    )
            
        if self.highlighted is not None:
            self.cells[self.highlighted].blit(self.surface)
            