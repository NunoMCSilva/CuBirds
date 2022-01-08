from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from random import randint, sample

from bird import Bird
from move import Move, Place
from side import Side


TABLE_ROWS, TABLE_COLS = 3, 4   # TODO: put inside Table class
STARTING_HAND_SIZE = 8


# TODO: put in it's own file
@dataclass
class Table:
    table: list[list[Bird]]

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


@dataclass
class Player:

    @dataclass
    class DictHand:
        dict_hand: dict[Bird, int] = field(
            default_factory=lambda: defaultdict(int))  # TODO: use defaultdict(int) as annot?

        def add(self, bird: Bird):
            self.dict_hand[bird] += 1

    id: int     # is this necessary?
    hand: DictHand = field(default_factory=DictHand)
    collection: DictHand = field(default_factory=DictHand)

    @property
    def bird_species_in_hand(self):
        return self.hand.dict_hand.keys()   # TODO: improve this a bit...

    def take_birds_from_hand(self, bird: Bird) -> list[Bird]:
        # TODO: ok, it needs some work, as well as dict hand -> remove to own file
        num = self.hand.dict_hand[bird]
        self.hand.dict_hand[bird] = 0
        return [bird] * num


Stage = Enum('State', 'PLACE')


@dataclass
class Game:
    num_players: int

    turn: int = field(default=None)
    stage: Stage = field(default=Stage.PLACE)

    players: list[Player] = field(default=None)
    table: Table = field(default=None)
    draw: list[Bird] = field(default=None)
    discard: list[Bird] = field(default_factory=list)

    def __post_init__(self):
        self.turn = self._get_random_turn(self.num_players)
        self.players = self._generate_players(self.num_players)

        deck = Bird.get_deck()
        self.table = self._lay_table(deck)
        self.draw = self._setup_draw(deck)

        self._deal_hands()
        self._deal_first_bird_to_collection()

        # TODO: add to tests: assert len(self.draw) == 110 - 3 * 4 - 2 * 8 - 2 * 1

    @property
    def current(self):
        # current player
        return self.players[self.turn]

    @staticmethod
    def _get_random_turn(num_players: int) -> int:
        return randint(0, num_players - 1)

    @staticmethod
    def _generate_players(num_players: int) -> list[Player]:
        return [Player(p) for p in range(num_players)]

    @staticmethod
    def _lay_table(deck: list[list[Bird]]) -> Table:
        def generate_table():
            # modifies deck inplace
            for _ in range(TABLE_ROWS):
                yield [birds.pop() for birds in sample(deck, TABLE_COLS)]

        return Table(list(generate_table()))

    @staticmethod
    def _setup_draw(deck: list[list[Bird]]) -> list[Bird]:
        def flatten_deck(d):
            return sum(d, [])

        def shuffle_deck(d):
            return sample(d, len(d))    # TODO: recheck this works

        return shuffle_deck(flatten_deck(deck))

    def _deal_hands(self) -> None:
        # modifies self.draw and self.players inplace
        for p in range(self.num_players):   # TODO: start with dealer?
            for _ in range(STARTING_HAND_SIZE):
                self.players[p].hand.add(self.draw.pop())

    def _deal_first_bird_to_collection(self) -> None:
        for p in range(self.num_players):   # TODO: start with dealer?
            # modifies self.draw and self.players inplace
            self.players[p].collection.add(self.draw.pop())

    def _get_legal_moves_place(self):   # TODO: yield
        for bird in self.current.bird_species_in_hand:
            for row in range(TABLE_ROWS):
                for side in Side:
                    yield Place(bird, row, side)

    # TODO: make this inner funtions of play?
    def _move_place(self, place: Place):
        """        num = self.current_player.take_birds(move.species)

        if (result := self.table.add_to_row(move.row, move.side, move.species, num)) is None:
            logging.info(f'Player #{self.current_player.id} places {num}{move.species!r} on {move.side!r} of row #{move.row} without surrounding')
            self.stage = 'Buy|Pass'
        else:
            raise NotImplementedError
        """
        birds = self.current.take_birds_from_hand(place.bird)
        self.table.add_to_row(birds, place.row, place.side)

    def get_legal_moves(self):  # TODO: -> yield
        if self.stage == Stage.PLACE:
            yield from self._get_legal_moves_place()
        else:
            raise NotImplementedError

    def play(self, move: Move):
        # TODO: verify move is present in legal moves
        if isinstance(move, Place):
            if self.stage == Stage.PLACE:
                self._move_place(move)
            else:
                raise ValueError(self.stage, move)  # TODO: improve exception
        else:
            raise NotImplementedError


def main():
    g = Game(2)
    print(g)

    lms = list(g.get_legal_moves())
    print(lms)
    move = lms[0]
    print(move)

    g.play(move)


if __name__ == '__main__':
    main()



'''    
    def get_legal_moves(self):
        elif self.stage == 'Buy|Pass':
            for mv in (Buy(), Pass()):
                yield mv
        else:
            raise NotImplementedError

    def play(self, move: Move):
        elif self.stage == 'Buy|Pass':
            if isinstance(move, Buy):
                self._buy()
            else:
                self._pass()
        else:
            raise NotImplementedError


    def _buy(self):
        s = set()
        for _ in range(2):
            c = self.draw.pop()
            self.current_player.add_to_hand(c)
            s.add(c)

        # TODO: don't complicate code to give better logging msgs...
        if len(s) == 1:
            logging.info(f'Player #{self.current_player.id} bought 2{c}')
        else:
            logging.info(f'Player #{self.current_player.id} bought {s}')

        self.turn = (self.turn + 1) % self.num_players
        self.stage = 'Place'

    def _pass(self):
        logging.info(f'Player #{self.current_player.id} passes')

        self.turn = (self.turn + 1) % self.num_players
        self.stage = 'Place'

    def _fly(self):
        raise NotImplementedError

'''


'''
from collections import defaultdict

import logging


from move import Move, Place, Fly, Buy, Pass
from side import Side
from species import Species
from utils import sample_with_repetition


logging.basicConfig(level=logging.DEBUG)


@dataclass
class Player:


    def take_birds(self, species: Species):
        num = self.hand[species]
        self.hand[species] = 0
        return num





def main():
    lms = list(g.get_legal_moves())
    print(lms)
    print(mv := lms[0])

    g.play(mv)

    lms = list(g.get_legal_moves())
    print(lms)
    print(mv := lms[0])

    g.play(mv)   # TODO: check if can Fly after Buy, I think not, but...
    print(g)

    lms = list(g.get_legal_moves())
    print(lms)
    print(mv := lms[0])

    g.play(mv)

    lms = list(g.get_legal_moves())
    print(lms)
    print(mv := lms[0])

    g.play(mv)


'''


"""
        for _ in range(10000):
            a, b, c = sample(deck, 3)
            assert len(set([a[0], b[0], c[0]])) == 3
            print(f"{a[0]!r}{b[0]!r}{c[0]!r}")

"""