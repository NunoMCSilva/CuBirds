from __future__ import annotations

from dataclasses import dataclass
from random import choice, sample
from typing import ClassVar, Optional

from bird import Bird
from move import Side, Place
from utils import count_adjacent


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
        #print(self.table[place.row], num, place)

        # add
        if place.side == Side.RIGHT:
            self.table[place.row], birds = self._add_right(self.table[place.row], num, place.bird)
        else:
            new_table_row, birds = self._add_right(list(reversed(self.table[place.row])), num, place.bird)
            self.table[place.row] = list(reversed(new_table_row))
            birds = None if birds is None else list(reversed(birds))   # not really necessary, but...

        return birds

    def is_single_species_in_row(self, row: int) -> bool:
        return set(self.table[row]) == 1

    def add_to_single_species_row(self, row: int, bird: Bird):
        # TODO: verify this in rulebook, each can be place by deal on either side
        # TODO: technically, dealer could choose how to add, giving him another way to improve his game
        if choice(list(Side)) == Side.RIGHT:  # TODO: add Side.random()?
            self.table[row] = self.table[row] + [bird]
        else:
            self.table[row] = [bird] + self.table[row]

        """
        import random
        print(random.choice(list(Side)))

        # TODO: row handling...
        print(self.table[place.row], birds)
        raise NotImplementedError
        """

    """
    @staticmethod
    def _add(table_row, num: int, bird: Bird, side: Side) -> Optional[list[Bird]]:
        def add_right() -> None:
            table_row.extend([place.bird] * num)

        def add_left(num: int, place: Place) -> None:
            # TODO: better than this?
            for _ in range(num):
                self.table[place.row].insert(0, place.bird)

        # TODO: refactor heavily
        try:
            # TODO: works on right...
            i = table_row.index(bird)
            inside = count_adjacent(table_row, bird, i)
            surrounded = table_row[i + inside:]

            if bird in surrounded:
                # e. g.: [N, N, F, O, N][N, N]  # how to handle... None? TODO: verify if possible
                raise NotImplementedError

            if surrounded:
                # e.g.: [N, N, F, O] [N, N] or [F, N, N, O] [N, N]
                #print(self.table[place.row], i, inside, surrounded)
                table_row = table_row[:i + inside] + [bird] * num
                #print(self.table[place.row])
                return surrounded
            else:
                # e.g. [F, O, N, N] [N, N]
                self._add_right(num, bird) if side == Side.RIGHT else self._add_left(num, bird)
                return None

    def add(self, num: int, place: Place) -> Optional[list[Bird]]:
        # TODO: refactor heavily -- this could work on table_row -- staticmethod _add(table_row, num, place)
        try:
            i = self.table[place.row].index(place.bird)
            inside = count_adjacent(self.table[place.row], place.bird, i)
            surrounded = self.table[place.row][i + inside:]

            if place.bird in surrounded:
                # e. g.: [N, N, F, O, N][N, N]  # how to handle... None? TODO: verify if possible
                raise NotImplementedError

            if surrounded:
                # e.g.: [N, N, F, O] [N, N] or [F, N, N, O] [N, N]
                #print(self.table[place.row], i, inside, surrounded)
                self.table[place.row] = self.table[place.row][:i + inside] + [place.bird] * num
                #print(self.table[place.row])
                return surrounded
            else:
                # e.g. [F, O, N, N] [N, N]
                self._add_right(num, place) if place.side == Side.RIGHT else self._add_left(num, place)
                return None

        except ValueError:
            # e.g. [F, O, P] [N, N]
            self._add_right(num, place) if place.side == Side.RIGHT else self._add_left(num, place)
            return None
    """

    """

    
    
    
    
    def _add_bird_not_in_row(self, num: int, bird: Bird, row: int, side: Side):
        # bird doesn't exist in row
        if side == Side.RIGHT:
            self.table[row].extend([bird] * num)
        else:
            # TODO: improve this one
            for _ in range(num):
                self.table[row].insert(0, bird)

        return None

    # TODO: better name? add_to_row?
    def add(self, num: int, bird: Bird, row: int, side: Side):  # TODO: -> Optional[
        if bird in self.table[row]:
            # bird exists in row

            if side == Side.RIGHT:
                i = self.table[row].index(bird)
                print(bird, self.table[row], i, self.table[row][i:])
                birds = self.table[row][i:]

                if set(birds) == {bird}:
                    # no surrounding other birds
                    return self._add_bird_not_in_row(num, bird, row, side)  # TODO: needs better name: no_surround
                else:
                    print(birds, self.table[row], self.table[row][i:], self.table[row][:i])

                    raise NotImplementedError
            else:
                raise NotImplementedError


            # TODO: implement this part
            return [Bird.FLAMINGO, Bird.FLAMINGO, Bird.MAGPIE]  # FIXME: WARNING: STUB
        else:
            return self._add_bird_not_in_row(num, bird, row, side)  # TODO: just use Move/Place?
    """

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