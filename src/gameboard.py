from typing import Optional, Iterator
from ship import Ship, Direction
from collections import OrderedDict
import random


class GameBoard:
    rows: int
    cols: int
    ships: Iterator[Ship]
    visible: bool

    current_ship: Optional[Ship]
    content: dict[tuple[int, int], Ship]
    ready: bool

    score: int
    hits: list[tuple[int, int]]
    misses: list[tuple[int, int]]
    reject: set[tuple[int, int]]

    def __init__(
            self,
            rows: int,
            cols: int,
            ships_lens: list[int],
            visible: bool = False
    ) -> None:
        
        self.rows = rows
        self.cols = cols
        self.ships = iter(Ship(len) for len in ships_lens)
        self.visible = visible

        self.current_ship = next(self.ships)
        self.content = dict()
        self.ready = False

        self.score = 0
        self.hits = []
        self.misses = []
        self.reject = set()

    
    def add(self, coordinates: tuple[int, int]) -> bool:
        if not self.validate(coordinates):
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
    

    def border(self, Ships: dict[tuple[int, int], Ship]) -> list[tuple[int, int]]:
        coords = set()

        for ship in Ships.values():
            for segment_coords in ship.segments.keys():
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        neighbor_coords = (segment_coords[0] + dx, segment_coords[1] + dy)

                        if neighbor_coords != segment_coords and\
                                neighbor_coords not in ship.segments and\
                                self.in_range(neighbor_coords):
                            
                            coords.add(neighbor_coords)

        return list(coords)


    def validate(self, coord: tuple[int, int]) -> bool:
        return (
            self.in_range(coord) and
            self.current_ship.check(coord) and
            coord not in self.content.keys() and
            coord not in self.border(self.content)
        )

    
    def random_run(self, length: int) -> list[tuple[int, int]]:
        while True:
            coord = self.random_coord()
            
            if not self.validate(coord):
                continue

            direction = self.random_direction()
            turn = random.choice([-1, 1])
            new_coords = [coord]

            for _ in range(length - 1):
                if direction == Direction.HORIZONTAL:
                    coord = (coord[0] + turn, coord[1])

                elif direction == Direction.VERTICAL:
                    coord = (coord[0], coord[1] + turn)

                if not self.validate(coord):
                    break

                new_coords.append(coord)   

            else:
                return new_coords

    
    def auto_place(self) -> None:
        while not self.ready:
            ship_coords = self.random_run(self.current_ship.length)

            for i in range(len(ship_coords)):
                self.current_ship.add(ship_coords[i], self.visible)
            
            self.update_content()
            self.current_ship = next(self.ships, None)

            if self.current_ship is None:
                self.ready = True

    
    def random_hit(self) -> tuple[int, int]:
        while True:
            coords = self.random_coord()
            if coords not in self.misses and coords not in self.hits and coords not in self.reject:
                return coords
            

    def create_hits_dict(self, enemy: 'GameBoard') -> dict[tuple[int, int], Ship]:
        hits_dict = {}

        for coord in self.hits:
            if coord in enemy.content.keys():
                hits_dict[coord] = enemy.content[coord]

        return hits_dict
            
    
    def find_hits_for_ship(self, dictionary: dict[tuple[int, int], Ship], ship: Ship) -> list[tuple[int, int]]:
        hits_for_ship = []

        for key, value in dictionary.items():
            if value is ship:
                hits_for_ship.append(key)

        return hits_for_ship
    

    def define_direction(self, first: tuple[int, int], second: tuple[int, int]) -> Direction:
        if first[0] == second[0]:
            return Direction.VERTICAL
        elif first[1] == second[1]:
            return Direction.HORIZONTAL
        else: return Direction.UNKNOWN


    def choose_possible_hit(self, old_coord: tuple[int, int], dx_values: list[int], dy_values: list[int]) -> tuple[int, int]:
        possible_hits = []

        for dx in dx_values:
            for dy in dy_values:
                if dy == 0 or dx == 0:
                    new_coord = (old_coord[0] + dx, old_coord[1] + dy)
                    if self.in_range(new_coord) and\
                            new_coord not in self.misses and\
                            new_coord not in self.reject and\
                            new_coord not in self.hits:
                        possible_hits.append(new_coord)

        if possible_hits:
            return random.choice(possible_hits)
        else:
            return None

    
    def smart_hit(self, enemy: 'GameBoard') -> tuple[int, int]:
        while True:
            hits_dict = self.create_hits_dict(enemy)
            ship_hits = self.find_hits_for_ship(hits_dict, enemy.content[self.hits[-1]])
            dx_values = [-1, 0, 1]
            dy_values = [-1, 0, 1]

            if len(ship_hits) > 1:
                first, second = self.hits[-2:]
                direction = self.define_direction(first, second)

                if direction == Direction.HORIZONTAL:
                    dx_values = [-1, 1]
                    dy_values = [0]

                elif direction == Direction.VERTICAL:
                    dx_values = [0]
                    dy_values = [-1, 1]

            for old_coord in ship_hits:
                possible_hit = self.choose_possible_hit(old_coord, dx_values, dy_values)
                if possible_hit:
                    return possible_hit


    def attack(self, enemy: 'GameBoard', coords: tuple[int, int] = None) -> bool:
        if not coords:
            if self.hits and not enemy.content[self.hits[-1]].sunken:
                coords = self.smart_hit(enemy)
            else:
                coords = self.random_hit()

        if coords in enemy.content:
            targeted_ship = enemy.content[coords]

            if targeted_ship.hit(coords):
                self.score += 1
                self.hits.append(coords)

                if targeted_ship.sunken:
                    border_coords = self.border(self.create_hits_dict(enemy))
                    self.reject.update(border_coords)

                return True
            
        else:
            self.misses.append(coords)
            return False
    
    
    def all_ships_sunk(self) -> bool:
        for ship in self.content.values():
            if not ship.sunken:
                return False

        return True
            