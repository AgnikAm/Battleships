from typing import Optional, Iterator

from ship import Ship


class GameBoard:
    rows: int
    cols: int
    ships: Iterator[Ship]
    current_ship: Optional[Ship]
    content: dict[tuple[int, int], Ship]
    ready: bool

    def __init__(
            self,
            rows: int,
            cols: int,
            ships_lens: list[int],
    ) -> None:
        
        self.rows = rows
        self.cols = cols
        self.ships = iter(Ship(len) for len in ships_lens)
        self.current_ship = next(self.ships)
        self.content = dict()
        self.ready = False
   

    def add(self, coordinates: tuple[int, int]) -> bool:
        if not self.current_ship.check(coordinates):
            return False
        
        self.current_ship.add(coordinates, True)

        if not self.current_ship.placed:
            return True
        
        self.update_content()
        self.current_ship = next(self.ships, None)

        if self.current_ship is None:
            self.ready = True

        return True


    def update_content(self) -> None:
        for coords in self.current_ship.coordinates:
            self.content[coords] = self.current_ship

    
    def auto_place(self, ships_lens: list[int]) -> None:
        pass
        
        
