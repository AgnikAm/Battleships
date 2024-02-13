import pygame
import sys
from draw_functions import draw_text
from ship import Ship


class GameBoard:
    def __init__(self, cell_size, x, y):
        self.grid_size = 10
        self.cell_size = cell_size
        self.x = x
        self.y = y
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.hovered_cell = None
        self.ships = []

    def draw_highlight(self, surface, color, row, col):
        rect = pygame.Rect(
            self.x + col * self.cell_size,
            self.y + row * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(surface, color, rect)

    def draw_board(self, surface):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                rect = pygame.Rect(
                    self.x + j * self.cell_size,
                    self.y + i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(surface, (255, 255, 255), rect, 1)

                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.hovered_cell = (i, j)

                if self.hovered_cell == (i, j):
                    self.draw_highlight(surface, (148, 124, 112), i, j)

                for ship in self.ships:
                    for pos in ship.positions:
                        self.draw_highlight(surface, (77, 54, 43), pos[0], pos[1])

    def asign_axes(self, surface):
        # rows
        for i in range(self.grid_size):
            number_text = str(i + 1)
            text_rect = pygame.Rect(
                self.x - self.cell_size,
                self.y + i * (self.cell_size),
                self.cell_size,
                self.cell_size
            )

            pygame.draw.rect(surface, (35, 87, 107), text_rect)
            draw_text(surface,
                      number_text,
                      None,
                      65,
                      (255, 255, 255),
                      text_rect.x + text_rect.width // 2,
                      text_rect.y + text_rect.height // 4)

        # cols
        for i in range(self.grid_size):
            letter_text = chr(ord('A') + i)
            text_rect = pygame.Rect(
                self.x + i * (self.cell_size),
                self.y - self.cell_size,
                self.cell_size,
                self.cell_size
            )

            pygame.draw.rect(surface, (35, 87, 107), text_rect)
            draw_text(surface,
                      letter_text,
                      None,
                      65,
                      (255, 255, 255),
                      text_rect.x + text_rect.width // 2,
                      text_rect.y + text_rect.height // 4)

    def place_ships(self, screen, background_surface):
        ship_number = 1
        for ship_length in [4, 3, 3, 3, 2, 2, 1, 1]:
            ship_placed = False
            ship = Ship(ship_length)
            pygame.display.flip()

            while not ship_placed:

                screen.blit(background_surface, (0, 0))
                for pos in ship.positions:
                    self.draw_highlight(background_surface, (77, 54, 43), pos[0], pos[1])

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.hovered_cell is not None:

                            if not any(pos == self.hovered_cell for pos in ship.positions):
                                ship.positions.append(self.hovered_cell)

                                if len(ship.positions) == ship_length:
                                    self.ships.append(ship)
                                    ship_placed = True
                                    ship_number += 1

                draw_text(screen, f"Place ship {ship_number}: ship of length {ship_length}", None, 50, (255, 255, 255),
                          pygame.display.Info().current_w // 2, 80)
                draw_text(screen, "Prepare for battle", None, 70, (255, 255, 255),
                          pygame.display.Info().current_w // 2, 20)
                self.draw_board(screen)
                self.asign_axes(screen)
                pygame.display.flip()

        return True
