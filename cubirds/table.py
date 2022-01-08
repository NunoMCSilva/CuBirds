from __future__ import annotations

from dataclasses import dataclass, field
from random import sample
from typing import ClassVar

from bird import Bird
from move import Side


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

    # TODO: better name? add_to_row?
    def add(self, num: int, bird: Bird, row: int, side: Side):  # TODO: -> Optional[
        if bird in self.table[row]:
            # bird exists in row

            # TODO: implement this part
            return [Bird.FLAMINGO, Bird.FLAMINGO, Bird.MAGPIE]  # FIXME: WARNING: STUB
        else:
            # bird doesn't exist in row
            if side == Side.RIGHT:
                self.table[row].extend([bird] * num)
            else:
                # TODO: improve this one
                for _ in range(num):
                    self.table[row].insert(0, bird)

            return None


'''

    def add_to_row(self, *args):        ### birds, row, side):
        raise NotImplementedError

        """
        if bird in self.table[row]:
            raise NotImplementedError
        else:
            if side == Side.RIGHT:
                self.table[row].extend(bird)
        """
'''
'''
@dataclass
class Table:
    table: list[list[Species]] = field(default=None)

    def add_to_row(self, row, side, species, num):
        # check presence
        surrounded = species in self.table[row]
        print(surrounded)

        def add(row, side, cards):
            if side == Side.LEFT:
                # TODO: needs work
                for c in cards:
                    row.insert(0, c)
            else:
                row.extend(cards)

        if surrounded:
            raise NotImplementedError
        else:
            add(self.table[row], side, [species] * num)
            return None

        """
        if surrounded:
            self.table[row].index(species)
            self.table[row].count(species)
        """
        """
        # add
        print(self.table[row])

        if side == Side.LEFT:
            # TODO: needs work
            for _ in range(num):
                self.table[row].insert(0, species)

            print(self.table[row])
        """

        """
        if side == Side.LEFT:
            # TODO: needs work
            start = num
            for _ in range(num):
                self.table[row].insert(0, species)
            print(start, self.table[row], self.table[row][start:])
        else:
            end = len(self.table[row])
            self.table[row].extend([species] * num)
            print(end, self.table[row], self.table[row][:end])

        if surrounded:
            print(self.table[row])
        else:
            return None
        """
'''