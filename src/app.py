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

ASSETS = 'assets'  # ścieżki do assetów przechowywać w stałych

BLANK = (255, 255, 255)


class State(Enum):
    MENU = auto()
    PLACEMENT = auto()
    MOVE = auto()
    AI_MOVE = auto()


class App:
    TITLE = 'Battleships'
    WINDOW_SIZE = 1024, 768 #1920, 1080
    FPS = 60

    state: State
    running: bool

    surface: Surface
    clock: Clock

    menu: MenuScreen
    placement: PlacementScreen
    game: GameScreen

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

    def clear(self) -> None:
        self.surface.fill(BLANK)

    def go_to_menu(self) -> None:
        self.state = State.MENU
        self.clear()

    def go_to_placement(self) -> None:
        # rozmieszczenie przez komputer
        # reszta kodu do przygotowania rozmieszczania przez gracza
        self.state = State.PLACEMENT
        self.clear()

    def go_to_game(self) -> None:
        self.clear()
        pass

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
