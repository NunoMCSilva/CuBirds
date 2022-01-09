from __future__ import annotations

from dataclasses import dataclass
from random import choice, sample
from typing import ClassVar, Optional

from .bird import Bird
from .move import Side, Place
from .utils import count_adjacent


@dataclass
class Table:
    table: list[list[Bird]]

    # TODO: not sure about the wisdom of this, but...
    NUM_ROWS: ClassVar[int] = 4
    NUM_COLS: ClassVar[int] = 3

    def __repr__(self):
        return repr(self.table)

    @staticmethod
    def generate_table(deck: list[list[Bird]]) -> Table:
        # modifies deck inplace
        return Table([[birds.pop() for birds in sample(deck, Table.NUM_COLS)] for _ in range(Table.NUM_ROWS)])

    @staticmethod
    def _add_right(table_row: list[Bird], num: int, bird: Bird) -> (list[Bird], Optional[list[Bird]]):
        try:
            pos = table_row.index(bird)
            inside = count_adjacent(table_row, bird, pos)
            surrounded = table_row[pos + inside:]

            if bird in surrounded:
                # e. g.: [N, N, F, O, N][N, N]  # how to handle... None? TODO: verify if possible
                raise NotImplementedError

            if surrounded:
                # e.g.: [N, N, F, O] [N, N] or [F, N, N, O] [N, N]
                return table_row[:pos + inside] + [bird] * num, surrounded
        except ValueError:
            pass

        # e.g. [F, O, N, N] [N, N]
        # e.g. [F, O, P] [N, N]
        return table_row + [bird] * num, None

    @staticmethod
    def _add_left(table_row: list[Bird], num: int, bird: Bird) -> (list[Bird], Optional[list[Bird]]):
        try:
            pos = table_row.index(bird)
        except ValueError:
            pass

        # e.g. [N, N] [N, N, O, F]
        # e. g. [N, N] [F, O, P]
        return [bird] * num + table_row, None

    def add(self, num: int, place: Place) -> Optional[list[Bird]]:
        if place.side == Side.RIGHT:
            self.table[place.row], birds = self._add_right(self.table[place.row], num, place.bird)
        else:
            new_table_row, birds = self._add_right(list(reversed(self.table[place.row])), num, place.bird)
            self.table[place.row] = list(reversed(new_table_row))
            birds = None if birds is None else list(reversed(birds))   # not really necessary, but...

        return birds

    def is_single_species_in_row(self, row: int) -> bool:
        return len(set(self.table[row])) == 1

    def add_to_single_species_row(self, row: int, bird: Bird):
        # TODO: verify this in rulebook, each can be place by deal on either side
        # TODO: technically, dealer could choose how to add, giving him another way to improve his game
        if choice(list(Side)) == Side.RIGHT:  # TODO: add Side.random()?
            self.table[row] = self.table[row] + [bird]
        else:
            self.table[row] = [bird] + self.table[row]
