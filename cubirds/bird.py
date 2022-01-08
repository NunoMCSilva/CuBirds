from __future__ import annotations

from enum import Enum, auto


class Bird(Enum):
    # first value is necessary to differentiate between birds
    # TODO:: auto() works to differentiate, but it doesn't create an int value, only <enum.auto object> check that
    FLAMINGO = (auto(), 2, 3, 7)
    OWL = (auto(), 3, 4, 10)
    TOUCAN = (auto(), 3, 4, 10)
    DUCK = (auto(), 4, 6, 13)
    PARROT = (auto(), 4, 6, 13)
    MAGPIE = (auto(), 5, 7, 17)
    NIGHTINGALE = (auto(), 6, 9, 20)
    ROBIN = (auto(), 6, 9, 20)

    def __init__(self, _, small_flock, big_flock, copies):
        self.small_flock = small_flock
        self.big_flock = big_flock
        self.copies = copies

    def __repr__(self):
        # this way it's smaller for lists
        return self.name[0]

    @staticmethod
    def get_deck():
        # a bit unusual, but this makes laying the table easier
        return [[b] * b.copies for b in Bird]
