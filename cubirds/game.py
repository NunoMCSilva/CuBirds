from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
import logging
from random import choice, randint
from typing import Union

from .bird import Bird
from .move import Side, Move, Place, Fly, Buy, Pass
from .player import Player
from .table import Table
from .utils import shuffle


#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


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

    _endgame: bool = field(default=False, repr=False)
    _game_winner: Player = field(default=None)

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
                self.players[p].hand.add(self._draw_card())

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

    """
    def _get_next_player(self) -> int:
        return (self.turn + 1) % self.num_players
    """

    def _next_turn(self) -> None:
        self.turn = (self.turn + 1) % self.num_players
        self.stage = Stage.PLACE

    def _new_round(self):
        # discard all hands
        for p in self.players:
            self.discard.extend(p.hand.reset())

        # "The game ends immediately if it is impossible for the dealer to deal 8 cards to (...)
        if len(self.draw) < self.num_players * Player.STARTING_HAND_SIZE:
            raise ValueError('insufficient cards')   # TODO: better exception
        else:
            self._deal_hands()

    def _draw_card(self) -> Bird:
        try:
            return self.draw.pop()
        except IndexError:
            self.draw = shuffle(self.discard)   # TODO: check rulebook, shuffle?
            self.discard = []

            return self.draw.pop()

    def _is_endgame(self):
        return self.current_player.collection.is_goal()

    def _calculate_game_winner(self):
        # endgame in case of insufficient cards
        """
        The game ends immediately if it is impossible for the dealer to deal 8 cards to
        each of the players even after reshuffling the discard pile into a new draw pile. The
        player with the most Bird cards in their collection then wins the game.
        In case of a tie, tied players share victory.
        """
        # TODO: improve this
        total = [(p.collection.total_birds, p) for p in self.players]
        max_ = max([tup[0] for tup in total])
        winners = [tup[1] for tup in total if tup[0] == max_]

        return winners[0] if len(winners) == 1 else winners

    # TODO: put this inside play?
    def _play_place(self, move: Place) -> None:
        num = self.current_player.hand.take(move.bird)
        birds = self.table.add(num, move)

        while self.table.is_single_species_in_row(move.row):
            self.table.add_to_single_species_row(move.row, self.draw.pop())

        # TODO: recheck this in rule book
        if birds is None:
            self.stage = Stage.BUY_OR_PASS
            logging.debug(f'Player #{self.turn} received no card from placement, it can now buy or pass')

            if not self.current_player.hand:
                try:
                    self._new_round()
                except ValueError:
                    self._endgame = True
                    self._game_winner = self._calculate_game_winner()
        else:
            self.current_player.hand.adds(birds)
            logging.debug(f'Player #{self.turn} received {birds} from placement')

            if flocks := self.current_player.hand.get_flocks():
                self.stage = Stage.FLY_OR_PASS
                logging.debug(f'Player #{self.turn} has {flocks} flock(s), it can now fly or pass')
            else:
                #turn = self.turn
                #self.turn = self._get_next_player()
                logging.debug(f'Player #{self.turn} has no flock(s)')    #, turn goes to player #{self.turn}')
                self._next_turn()

    def _play_fly(self, move: Fly) -> None:
        num = self.current_player.hand.take(move.bird)
        if num >= move.bird.big_flock:
            self.current_player.collection.adds([move.bird] * 2)
            self.discard.extend([move.bird] * (num - 2))
        elif num >= move.bird.small_flock:
            self.current_player.collection.add(move.bird)
            self.discard.extend([move.bird] * (num - 1))
        else:
            raise ValueError('should be possible to flock')

        if self._is_endgame():
            self._endgame = True
            self._game_winner = self.current_player
            return

        if not self.current_player.hand:
            try:
                self._new_round()
            except ValueError:
                self._endgame = True
                self._game_winner = self._calculate_game_winner()
                return

        #self.turn = self._get_next_player()
        self._next_turn()

    def _play_buy(self) -> None:
        self.current_player.hand.adds([self._draw_card() for _ in range(2)])
        # TODO: log: player buys 2 cards - TODO: check boardcardgame for inspiration on msgs
        logging.debug(f"Player {self.turn} buys two cards")
        #self.turn = self._get_next_player()     # pass -- TODO: Pass.run() idea
        self._next_turn()

    def _play_pass(self) -> None:
        self._next_turn()

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
            elif isinstance(move, Pass):
                self._play_pass()
            else:
                raise ValueError('illegal move class', move)  # TODO: improve exception
        else:
            raise ValueError('illegal move', move)  # TODO: improve exception

    def is_endgame(self) -> bool:
        return self._endgame

    def get_winner(self) -> Union[Player, list[Player]]:
        return self._game_winner


def main():
    g = Game(num_players=2)
    print(g)

    while not g.is_endgame():
        move = choice(list(g.get_legal_moves()))    # TODO: add random_play?
        print(move)

        g.play(move)
        print(g)

    print(g)
    print('Winner(s) =', g.get_winner())

    """
    lms = list(g.get_legal_moves())
    print(lms)
    move = choice(lms)
    print(move)

    g.play(move)
    print(g)

    lms = list(g.get_legal_moves())
    print(lms)
    move = choice(lms)
    print(move)

    g.play(move)
    print(g)

    if g.current_player.\:
        print(g.current_player.hand, bool(g.current_player.hand), bool(Player(2).hand))
    """


if __name__ == '__main__':
    main()
