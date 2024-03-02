from enum import Enum, auto
from dataclasses import dataclass


class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()
    UNKNOWN = auto()


@dataclass
class Segment:
    coordinates: tuple[int, int]
    destroyed: bool
    visible: bool


class Ship:
    length: int
    direction: Direction
    segments: dict[tuple[int, int], Segment]
    placed: bool
    sunken: bool


    def __init__(
            self,
            length: int
    ) -> None:
        
        self.length = length
        self.direction = Direction.UNKNOWN
        self.segments = dict()
        self.placed = False
        self.sunken = False


    def add(self, coordinates: tuple[int, int], visible: bool) -> None:
        self.segments[coordinates] = Segment(coordinates, False, visible)
        self.update_direction()
        self.update_placed()


    def update_placed(self) -> None:
        self.placed = self.length == len(self.segments)

    
    def update_direction(self) -> None:
        if len(self.segments) !=2:
            return
        
        first, second = self.segments.keys()

        if first[0] == second[0]:
            self.direction = Direction.VERTICAL
        elif first[1] == second[1]:
            self.direction = Direction.HORIZONTAL

    
    def check(self, coordinates: tuple[int, int]) -> bool:
        if coordinates in self.segments:
            return False
        
        coords = self.segments.keys() # (col, row)

        match self.direction:
            case Direction.UNKNOWN if len(self.segments) == 0:
                return True
            
            case Direction.UNKNOWN:
                element = list(coords)[0]

                return (
                    element[1] == coordinates[1] and
                    (element[0] == coordinates[0] + 1 or element[0] == coordinates[0] - 1)
                ) or (
                    element[0] == coordinates[0] and
                    (element[1] == coordinates[1] + 1 or element[1] == coordinates[1] - 1)
                )
            
            case Direction.VERTICAL:
                upper = min(coords, key=lambda pos: pos[1])
                lower = max(coords, key=lambda pos: pos[1])

                return coordinates[0] == upper[0] and (
                    coordinates[1] == upper[1] - 1 or
                    coordinates[1] == lower[1] + 1
                )
            
            case Direction.HORIZONTAL:
                left = min(coords, key=lambda pos: pos[0])
                right = max(coords, key=lambda pos: pos[0])

                return coordinates[1] == left[1] and (
                    coordinates[0] == left[0] - 1 or
                    coordinates[0] == right[0] + 1
                )
            

    def update_sunken(self) -> None:
        if all(segment.destroyed for segment in self.segments.values()):
            self.sunken = True

    
    def hit(self, coords: tuple[int, int]) -> bool:
        segment = self.segments[coords]

        if not segment or segment.destroyed:
            return False
        
        segment.destroyed = True
        self.update_sunken()
        return True
    
            
    @property
    def coordinates(self) -> list[tuple[int, int]]:
        return list(self.segments.keys())

        

    