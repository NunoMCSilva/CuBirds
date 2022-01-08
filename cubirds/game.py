from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
import logging
from random import choice, randint

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
        birds = self.table.add(num, move)

        while self.table.is_single_species_in_row(move.row):
            self.table.add_to_single_species_row(move.row, self.draw.pop())

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
        num = self.current_player.hand.take(move.bird)
        if num >= move.bird.big_flock:
            self.current_player.collection.adds([move.bird] * 2)
            self.discard.extend([move.bird] * (num - 2))
        elif num >= move.bird.small_flock:
            self.current_player.collection.add(move.bird)
            self.discard.extend([move.bird] * (num - 1))
        else:
            raise ValueError('should be possible to flock')

        self.turn = self._get_next_player()

    def _play_buy(self):
        self.current_player.hand.adds([self.draw.pop() for _ in range(2)])
        # TODO: log: player buys 2 cards - TODO: check boardcardgame for inspiration on msgs
        logging.debug(f"Player {self.turn} buys two cards")
        self.turn = self._get_next_player()     # pass -- TODO: Pass.run() idea

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
