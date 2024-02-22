from typing import Optional, Iterator
from ship import Ship, Direction
import random


class GameBoard:
    rows: int
    cols: int
    ships: Iterator[Ship]
    current_ship: Optional[Ship]
    content: dict[tuple[int, int], Ship]
    ready: bool
    debug: bool

    def __init__(
            self,
            rows: int,
            cols: int,
            ships_lens: list[int],
            debug: bool
    ) -> None:
        
        self.rows = rows
        self.cols = cols
        self.ships = iter(Ship(len) for len in ships_lens)
        self.current_ship = next(self.ships)
        self.content = dict()
        self.ready = False
        self.debug = debug

    
    def add(self, coordinates: tuple[int, int]) -> bool:
        if not self.validate_coord(coordinates):
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


    def random_coord(self) -> tuple[int, int]:
        col = random.randint(0, self.cols-1)
        row = random.randint(0, self.rows-1)

        return col, row
    

    def random_direction(self) -> Direction:
        return random.choice([Direction.HORIZONTAL, Direction.VERTICAL])
    

    def in_range(self, coord: tuple[int, int]) -> bool:
        col, row = coord
        return 0 <= col <= self.cols-1 and 0 <= row <= self.rows-1
    

    def border_coords(self) -> list[tuple[int, int]]:
        border_coordinates = set()
        for ship in self.content.values():
            for segment_coords, segment in ship.segments.items():
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        neighbor_coords = (segment_coords[0] + dx, segment_coords[1] + dy)
                        if (neighbor_coords != segment_coords and
                                neighbor_coords not in ship.segments and
                                self.in_range(neighbor_coords)
                        ):
                            border_coordinates.add(neighbor_coords)
        return list(border_coordinates)


    def validate_coord(self, coord: tuple[int, int]) -> bool:
        return (
            self.in_range(coord) and
            self.current_ship.check(coord) and
            coord not in self.content.keys() and
            coord not in self.border_coords()
        )

    
    def random_run(self, len) -> list[tuple[int, int]]:
        while True:
            coord = self.random_coord()
            if not self.validate_coord(coord):
                continue
            direction = self.random_direction()
            turn = random.choice([-1, 1])
            new_coords = [coord]

            for _ in range(len - 1):
                if direction == Direction.HORIZONTAL:
                    coord = (coord[0] + turn, coord[1])
                elif direction == Direction.VERTICAL:
                    coord = (coord[0], coord[1] + turn)

                if not self.validate_coord(coord):
                    break
                new_coords.append(coord)   

            else:
                return new_coords

    
    def auto_place(self) -> None:
        while not self.ready:
            ship_coords = self.random_run(self.current_ship.length)

            for i in range(len(ship_coords)):
                self.current_ship.add(ship_coords[i], self.debug)
            
            self.update_content()
            self.current_ship = next(self.ships, None)

            if self.current_ship is None:
                self.ready = True