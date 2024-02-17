from typing import Optional

from ship import Ship


class GameBoard:
    rows: int
    cols: int
    ships_lens: list[int]
    ships: list[Ship]
    content: dict[tuple[int, int], Ship]

    def __init__(
            self,
            rows: int,
            cols: int,
            ships_lens: list[int],
    ) -> None:
        
        self.rows = rows
        self.cols = cols
        self.ships_lens = ships_lens
        self.ships = []

        for ship_len in ships_lens:
            self.ships.append(Ship(ship_len))

        self.content = dict(
            ((row, col), None)
            for row in range(rows)
            for col in range(cols)
        )

    def is_ready(self) -> bool:
        return not any(ship.placed == False for ship in self.ships)

    def update_content(self) -> None:
        # uaktualnienie słownika content po ułożeniu statków
        for pos in self.content.keys():
            for ship in self.ships:
                if pos in ship.coordinates:
                    self.content[pos] = ship
        
