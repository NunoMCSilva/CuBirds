from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
import logging
from random import randint

from bird import Bird
from move import Side, Move, Place, Fly, Buy, Pass
from player import Player
from table import Table
from utils import shuffle


logging.basicConfig(level=logging.DEBUG)


class Stage(Enum):
    PLACE = auto()
    BUY_OR_PASS = auto()
    FLY_OR_PASS = auto()

    # TODO: create a Enum class in utils that already has this?
    def __repr__(self):
        return self.name.capitalize()   # TODO: Buy_or_pass => BuyOrPass OR Buy_or_Pass


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
        self.players = Player.generate_players(self.num_players)

        deck = Bird.get_deck()
        self.table = Table.generate_table(deck)
        self.draw = self._setup_draw(deck)

        self._deal_hands()
        self._deal_first_bird_to_collection()

    @property
    def current_player(self):
        return self.players[self.turn]

    @staticmethod
    def _get_random_turn(num_players: int) -> int:
        return randint(0, num_players - 1)

    @staticmethod
    def _setup_draw(deck: list[list[Bird]]) -> list[Bird]:
        def flatten_deck(d):
            return sum(d, [])

        return shuffle(flatten_deck(deck))

    def _deal_hands(self) -> None:
        # modifies self.draw and self.players in place
        for p in range(self.num_players):       # TODO: start with dealer?
            for _ in range(Player.STARTING_HAND_SIZE):
                self.players[p].hand.add(self.draw.pop())

    def _deal_first_bird_to_collection(self) -> None:
        # modifies self.draw and self.players inplace
        for p in range(self.num_players):   # TODO: start with dealer?
            self.players[p].collection.add(self.draw.pop())

    # TODO: put this inside get_legal_moves?
    def _get_legal_moves_place(self):  # TODO: -> yield
        for bird in self.current_player.hand.get_species():
            for row in range(Table.NUM_ROWS):
                for side in Side:
                    yield Place(bird, row, side)

    def _get_next_player(self) -> int:
        return (self.turn + 1) % self.num_players

    # TODO: put this inside play?
    def _play_place(self, move: Place):
        num = self.current_player.hand.take(move.bird)
        birds = self.table.add(num, move.bird, move.row, move.side)

        # TODO: recheck this in rule book
        if birds is None:
            self.stage = Stage.BUY_OR_PASS
            logging.debug(f'Player #{self.turn} received no card from placement, it can now buy or pass')
        else:
            self.current_player.hand.adds(birds)
            logging.debug(f'Player #{self.turn} received {birds} from placement')

            if flocks := self.current_player.hand.get_flocks():
                self.stage = Stage.FLY_OR_PASS
                logging.debug(f'Player #{self.turn} has {flocks} flock(s), it can now fly or pass')
            else:
                turn = self.turn
                self.turn = self._get_next_player()
                logging.debug(f'Player #{turn} has no flock(s), turn goes to player #{self.turn}')

    def _play_fly(self, move: Fly):
        raise NotImplementedError

    def _play_buy(self):
        raise NotImplementedError

    @staticmethod
    def _get_legal_moves_buy_or_pass():
        # TODO: improve this...
        yield Buy()
        yield Pass()

    def _get_legal_moves_fly_or_pass(self):
        for bird in self.current_player.hand.get_flocks():
            yield Fly(bird)
        yield Pass()

    def get_legal_moves(self):  # TODO: -> yield
        # TODO: improve this
        if self.stage == Stage.PLACE:
            yield from self._get_legal_moves_place()
        elif self.stage == Stage.BUY_OR_PASS:
            yield from self._get_legal_moves_buy_or_pass()
        elif self.stage == Stage.FLY_OR_PASS:
            yield from self._get_legal_moves_fly_or_pass()
        else:
            raise NotImplementedError

    def play(self, move: Move):
        if move in self.get_legal_moves():
            if isinstance(move, Place):
                self._play_place(move)
            elif isinstance(move, Fly):
                self._play_fly(move)
            elif isinstance(move, Buy):
                self._play_buy()
            else:
                raise NotImplementedError
        else:
            raise ValueError('illegal move', move)  # TODO: improve exception

        """
        # TODO: improve this... should need so many ifs
        if move in self.get_legal_moves():  # TODO: optimized this: a cache?
            # TODO: it would be nice not to need isinstance here
            if isinstance(move, Place):
                if self.stage == Stage.PLACE:
                    self._play_place(move)
                else:
                    # TODO: can this even happen, with the get_legal_move verification?
                    raise ValueError('wrong stage', self.stage, move)  # TODO: improve exception
            elif isinstance(move, Fly):
                if self.stage == Stage.FLY_OR_PASS:
                    self._play_fly(move)
            elif isinstance(move, Buy):
                if self.stage == Stage.BUY_OR_PASS:
                    self._play_buy()
            else:
                raise NotImplementedError
        """


def main():
    g = Game(num_players=2)
    print(g)

    lms = list(g.get_legal_moves())
    print(lms)
    move = lms[0]
    print(move)

    g.play(move)
    print(g)

    lms = list(g.get_legal_moves())
    print(lms)
    move = lms[0]
    print(move)

    g.play(move)
    print(g)


if __name__ == '__main__':
    main()



'''


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