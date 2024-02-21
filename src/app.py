from collections.abc import Callable
from typing import Any, Iterable, Mapping

import pygame
from pygame import Surface, Rect
from pygame.time import Clock

from enum import Enum, auto

from dataclasses import dataclass
from abc import ABC, abstractmethod

from placement import PlacementScreen
from menu import MenuScreen
from game import GameScreen
from gameboard import GameBoard

from drawing import WHITE

ASSETS = 'assets'  # ścieżki do assetów przechowywać w stałych

class State(Enum):
    MENU = auto()
    PLACEMENT = auto()
    MOVE = auto()
    AI_MOVE = auto()


class App:
    TITLE = 'Battleships'
    WINDOW_SIZE = 1920, 1020 # 1024, 768
    FPS = 60
    BOARD_SIZE = 10, 10
    SHIPS_LENS = [4, 3, 2, 2, 1, 1]

    state: State
    running: bool

    surface: Surface
    clock: Clock

    menu: MenuScreen
    placement: PlacementScreen
    game: GameScreen

    player: GameBoard
    enemy: GameBoard

    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        pygame.display.set_caption(App.TITLE)

        self.surface = pygame.display.set_mode(
            App.WINDOW_SIZE, 
            pygame.RESIZABLE
        )

        self.clock = Clock()

        self.state = State.MENU
        self.running = False

        self.menu = MenuScreen(self.surface)
        self.placement = PlacementScreen(self.surface)
        self.game = GameScreen(self.surface)

        self.player = GameBoard(
            *App.BOARD_SIZE,
            App.SHIPS_LENS
        )

        self.enemy = GameBoard(
            *App.BOARD_SIZE,
            App.SHIPS_LENS
        )

    def clear(self) -> None:
        self.surface.fill(WHITE)

    def go_to_menu(self) -> None:
        self.state = State.MENU
        self.clear()

    def go_to_placement(self) -> None:
        self.enemy.auto_place(App.SHIPS_LENS)
        # reszta kodu do przygotowania rozmieszczania przez gracza
        self.state = State.PLACEMENT
        self.clear()

    def go_to_game(self) -> None:
        self.clear()
        self.state = State.MOVE

    def quit(self) -> None:
        self.running = False

    def handle_events(self) -> None:
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False

                case pygame.MOUSEBUTTONDOWN if self.state == State.MENU:
                    if self.menu.start.rect.collidepoint(mouse):
                        self.go_to_placement()

                    elif self.menu.quit.rect.collidepoint(mouse):
                        self.quit()

                case pygame.MOUSEBUTTONDOWN if self.state == State.PLACEMENT:
                    if self.placement.menu.collidepoint(mouse):
                        self.go_to_menu()

                    elif coords := self.placement.collide_field(mouse):
                        self.player.add(coords) and self.placement.place_ship(coords)
                        
                case pygame.MOUSEMOTION if self.state == State.PLACEMENT:
                    if coords := self.placement.collide_field(mouse):
                        self.placement.grid.highlight(coords)
                        
                    else:
                        self.placement.grid.highlighted = None

                    # elif inne rzeczy
                        
                case pygame.MOUSEBUTTONDOWN if self.state == State.MOVE:
                    pass

                case _:
                    pass

    def handle_state(self) -> None:
        match self.state:
            case State.MENU:
                self.menu.draw()

            case State.PLACEMENT:
                self.placement.draw()
                if self.player.ready:
                    self.go_to_game()
                
            case State.MOVE:
                pass

            case State.AI_MOVE:
                pass

    def run(self) -> None:
        self.running = True

        while self.running:
            self.handle_events()
            self.handle_state()
            pygame.display.flip()
            
        # coś na koniec

if __name__ == '__main__':
    app = App()
    app.run()
