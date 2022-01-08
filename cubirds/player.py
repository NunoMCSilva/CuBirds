from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import ClassVar

from bird import Bird


# TODO: DictBirds superclass of Hand and Collection
@dataclass
class Hand:
    # TODO: can I use defaultdict(int) as annotation?
    hand: dict = field(default_factory=lambda: defaultdict(int))

    def __bool__(self):
        return bool(self.hand)

    def __repr__(self):
        return repr([[b] * n for b, n in self.hand.items()])

    def add(self, bird: Bird):
        self.hand[bird] += 1

    # TODO: needs better name
    def adds(self, birds: list[Bird]):
        for b in birds:
            self.add(b)

    def get_species(self):  # TODO: add ->, TODO: better name? get_species_in_hand?
        return self.hand.keys()

    def take(self, bird: Bird) -> int:
        num = self.hand[bird]
        del self.hand[bird]
        return num

    def get_flocks(self) -> list[Bird]:
        # TODO: can be improved?
        def flocks():
            for b, n in self.hand.items():
                if n >= b.small_flock:
                    yield b

        return list(flocks())

    def reset(self) -> list[Bird]:
        # TODO: improve this
        birds = []
        for bird in list(self.get_species()):
            num = self.take(bird)
            birds.extend([bird] * num)
        return birds


@dataclass
class Collection:
    # TODO: can I use defaultdict(int) as annotation?
    collection: dict = field(default_factory=lambda: defaultdict(int))

    def __repr__(self):
        return ', '.join(f'{b!r}:{n}' for b, n in self.collection.items())

    @property
    def total_birds(self):
        return sum(self.collection.values())

    def add(self, bird: Bird):
        self.collection[bird] += 1

    # TODO: needs better name
    def adds(self, birds: list[Bird]):
        for b in birds:
            self.add(b)

    def get_species(self):  # TODO: add ->, TODO: better name? get_species_in_hand?
        return self.collection.keys()

    def is_goal(self) -> bool:
        # TODO: add values to constants
        return len(self.get_species()) == 7 or len([b for b, n in self.collection.items() if n >= 3]) >= 2


@dataclass
class Player:
    id: int     # is this necessary?
    hand: Hand = field(default_factory=Hand)
    collection: Collection = field(default_factory=Collection)

    # TODO: not sure about the wisdom of this, but...
    STARTING_HAND_SIZE: ClassVar[int] = 8

    @staticmethod
    def generate_players(num_players: int) -> list[Player]:
        # return list(map(Player, range(num_players)))
        return [Player(p) for p in range(num_players)]
