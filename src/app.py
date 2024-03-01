import pygame
from pygame import Surface
from pygame.time import Clock

from enum import Enum, auto

from menu import MenuScreen
from placement import PlacementScreen
from game import GameScreen
from gameboard import GameBoard

from drawing import WHITE


class State(Enum):
    MENU = auto()
    PLACEMENT = auto()
    MOVE = auto()
    ENEMY_MOVE = auto()

class App:
    TITLE = 'Battleships'
    WINDOW_SIZE = 1920, 1020
    FPS = 60
    BOARD_SIZE = 10, 10
    SHIPS_LENS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    TEST = True

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
        self.game = GameScreen(self.surface, self.placement.grid.occupied)

        self.player = GameBoard(
            *App.BOARD_SIZE,
            App.SHIPS_LENS,
            True
        )

        self.enemy = GameBoard(
            *App.BOARD_SIZE,
            App.SHIPS_LENS,
            self.TEST
        )


    def clear(self) -> None:
        self.player = GameBoard(
            *App.BOARD_SIZE,
            App.SHIPS_LENS,
        )
        self.enemy = GameBoard(
            *App.BOARD_SIZE,
            App.SHIPS_LENS,
            self.TEST
        )
        self.placement = PlacementScreen(self.surface)
        self.game = GameScreen(self.surface, self.placement.grid.occupied)


    def to_menu(self) -> None:
        self.state = State.MENU
        self.clear()
    

    def to_placement(self) -> None:
        self.enemy.auto_place()
        self.game.update_ships(self.game.grid_enemy, self.enemy)
        self.state = State.PLACEMENT


    def to_move(self) -> None:
        self.state = State.MOVE

    
    def to_enemy_move(self) -> None:
        self.state = State.ENEMY_MOVE

        self.game.draw()
        self.enemy.attack(self.player)
        for hit in self.enemy.hits:
            self.game.grid_player.mark_hit(hit)
        for miss in self.enemy.misses:
            self.game.grid_player.mark_miss(miss)
        self.to_move()


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
                        self.to_placement()
                    
                    if self.menu.quit.rect.collidepoint(mouse):
                        self.quit()

                case pygame.MOUSEBUTTONDOWN if self.state == State.PLACEMENT:
                    if self.placement.menu_icon_rect.collidepoint(mouse):
                        self.to_menu()

                    if self.placement.retry_icon_rect.collidepoint(mouse):
                        self.clear()

                    if self.placement.auto_place.collidepoint(mouse):
                        self.clear()
                        self.enemy.auto_place()
                        self.game.update_ships(self.game.grid_enemy, self.enemy)
                        self.player.auto_place()
                        for coords in self.player.content.keys():
                            self.placement.place_ship(coords)

                    if self.placement.accept_icon_rect.collidepoint(mouse) and self.player.ready:
                        self.to_move()

                    if (coords := self.placement.collide_field(mouse)) and not self.player.ready:
                        self.player.add(coords) and self.placement.place_ship(coords)

                case pygame.MOUSEMOTION if self.state == State.PLACEMENT:
                    if coords := self.placement.collide_field(mouse):
                        self.placement.grid.highlight(coords)
                        
                    else:
                        self.placement.grid.highlighted = None

                case pygame.MOUSEBUTTONDOWN if self.state == State.MOVE:
                    if self.game.menu_icon_rect.collidepoint(mouse):
                        self.to_menu()

                    if coords := self.game.collide_field(mouse):
                        if self.player.attack(self.enemy, coords):
                            self.game.grid_enemy.mark_hit(coords)
                        else:
                            self.game.grid_enemy.mark_miss(coords)

                        pygame.display.flip()
                        self.to_enemy_move()

                case pygame.MOUSEMOTION if self.state == State.MOVE:
                    if coords := self.game.collide_field(mouse):
                        self.game.grid_enemy.highlight(coords)
                        
                    else:
                        self.game.grid_enemy.highlighted = None

                case pygame.MOUSEBUTTONDOWN if self.state == State.ENEMY_MOVE:
                    if self.game.menu_icon_rect.collidepoint(mouse):
                        self.to_menu()


    def handle_state(self) -> None:
        match self.state:
            case State.MENU:
                self.menu.draw()

            case State.PLACEMENT:
                if self.player.current_ship:
                    self.placement.set_header(self.player.current_ship.length)
                else:
                    self.placement.set_header(None)
                self.placement.draw()
                
            case State.MOVE:
                self.game.draw()

            case State.ENEMY_MOVE:
                pass


    def run(self) -> None:
        self.running = True

        while self.running:
            self.handle_events()
            self.handle_state()
            pygame.display.flip()

    
if __name__ == '__main__':
    app = App()
    app.run()
