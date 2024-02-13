from collections.abc import Callable
from typing import Any, Iterable, Mapping

import pygame
from pygame import Surface, Rect
from pygame.time import Clock

from threading import Thread
from enum import Enum, auto

from dataclasses import dataclass
from abc import ABC, abstractmethod

ASSETS = 'assets'  # ścieżki do assetów przechowywać w stałych


class State(Enum):
    MENU = auto()
    PLACEMENT = auto()
    MOVE = auto()
    AI_MOVE = auto()


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

    def hide(self) -> None:
        pass


class PlacementScreen:
    surface: Surface
    menu: Rect

    def draw(self) -> None:
        pass


class GameScreen:
    surface: Surface

    def draw(self) -> None:
        pass


class App(Thread):
    TITLE = 'Battleships'
    WINDOW_SIZE = 1920, 1080
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

    def go_to_menu(self) -> None:
        self.state = State.MENU

    def go_to_placement(self) -> None:
        # rozmieszczenie przez komputer
        # reszta kodu do przygotowania rozmieszczania przez gracza
        self.state = State.PLACEMENT

    def go_to_game(self) -> None:
        pass

    def quit(self) -> None:
        self.running = False

    def run(self) -> None:
        self.running = True

        while self.running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False

                    case pygame.MOUSEBUTTONDOWN if self.state == State.MENU:
                        mouse = pygame.mouse.get_pos()

                        if self.menu.start.collidepoint(mouse):
                            self.go_to_placement()

                        elif self.menu.quit.collidepoint(mouse):
                            self.quit()

                    case pygame.MOUSEBUTTONDOWN if self.state == State.PLACEMENT:
                        if self.placement.menu.collidepoint(mouse):
                            self.go_to_menu()

                        # elif inne rzeczy

                    case _:
                        pass

            match self.state:
                case State.MENU:
                    self.menu.draw()

                case State.PLACEMENT:
                    self.placement.draw()

                case State.MOVE:
                    pass

                case State.AI_MOVE:
                    pass

        # coś na koniec

if __name__ == '__main__':
    app = App()
    app.run()
    app.join()
