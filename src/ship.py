from typing import Optional


class Ship:
    length: int
    coordinates: Optional[list[tuple[int, int]]]
    placed: bool
    health: int
    sunken: bool
    visibility: bool

    def __init__(
            self,
            length: int,
    ) -> None:
        
        self.length = length
        self.coordinates = []
        self.placed = False
        self.health = length
        self.sunken = False

    
    def add_coordinate(self, cell: tuple[int, int]) -> None:
        self.coordinates.append(cell)
        if len(self.coordinates) == self.length:
            self.placed = True


    def hit(self) -> None:
        self.health -= 1
        if self.health == 0:
            self.sunken = True