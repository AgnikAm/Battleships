import pygame
from pygame import Surface, Rect, draw
from component import Component
from typing import Optional

from drawing import draw_text, draw_full_rect
from drawing import WHITE, CHATHAMS_BLUE

class Grid:
    surface: Surface
    size: tuple[int, int]
    cols: int
    rows: int
    upperleft: tuple[int, int]
    cell_size: int
    cell_color: tuple[int, int, int]
    highlighted_color: tuple[int, int, int]

    cells: dict[tuple[int, int], Component]
    highlighted_cells: dict[tuple[int, int], Component]
    axis_x: Rect
    col_labels: dict
    axis_y: Rect
    row_labels: dict

    highlighted: Optional[tuple[int, int]]
    occupied: Optional[dict[tuple[int, int]]]


    def __init__(
            self, 
            surface: Surface,
            size: tuple[int, int],
            cols: int,
            rows: int,
            upperleft: tuple[int, int],
            cell_size: int, 
            cell_color: tuple[int, int, int],
            highlighted_color: tuple[int, int, int]
    ) -> None:
        
        self.surface = surface
        self.size = size
        self.cols = cols
        self.rows = rows
        self.upperleft = upperleft
        self.cell_size = cell_size
        self.cell_color = cell_color
        self.highlighted_color = highlighted_color


        self.cells = dict(
            ((row, col), draw_full_rect(cell_size, cell_color, upperleft, (row, col)))
            for row in range(rows)
            for col in range(cols)
        )

        self.highlighted_cells = dict(
            ((row, col), draw_full_rect(cell_size, highlighted_color, upperleft, (row, col)))
            for row in range(rows)
            for col in range(cols)
        )

        self.axis_x = Rect(
            upperleft[0],
            upperleft[1] - cell_size,
            cell_size * cols,
            cell_size
        )

        self.col_labels = dict(
            (col, chr(ord('A') + col))
            for col in range(cols)
        )

        self.axis_y = Rect(
            upperleft[0] - cell_size,
            upperleft[1],
            cell_size,
            cell_size * rows
        )

        self.row_labels = dict(
            (row, str(row + 1))
            for row in range(rows)
        )

        self.highlighted = None

        self.occupied = dict(
            ((row, col), False)
            for row in range(rows)
            for col in range(cols)
        )
        

    def highlight(self, cell: tuple[int, int]) -> None:
        self.highlighted = cell


    def draw_cols(self, col: int) -> Component:

        centerx = self.axis_x.x + col * self.cell_size + self.cell_size // 2
        centery = self.axis_x.y + self.cell_size // 4

        return draw_text(self.col_labels[col],
                         None,
                         int(self.size[1] * 0.08),
                         WHITE,
                         (centerx, centery)
        )
    

    def draw_rows(self, row: int) -> Component:

        centerx = self.axis_y.x + self.cell_size // 2
        centery = self.axis_y.y + row * self.cell_size + self.cell_size // 4

        return draw_text(self.row_labels[row],
                         None,
                         int(self.size[1] * 0.08),
                         WHITE,
                         (centerx, centery)
        )


    def draw(self) -> None:

        draw.rect(self.surface, CHATHAMS_BLUE, self.axis_x)
        draw.rect(self.surface, CHATHAMS_BLUE, self.axis_y)

        for i in range(self.cols):
            self.draw_cols(i).blit(self.surface)
        for i in range(self.rows):
            self.draw_rows(i).blit(self.surface)

        for cell in self.cells.values():
            draw.rect(self.surface,
                      WHITE,
                      cell.rect,
                      1
            )

        for cell in self.cells.keys():
            if self.occupied[cell]:
                self.cells[cell].blit(self.surface)
            
        if self.highlighted is not None:
            self.highlighted_cells[self.highlighted].blit(self.surface)
            