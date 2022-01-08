from __future__ import annotations

from enum import Enum, auto


class Bird(Enum):
    # first value is necessary to differentiate between birds
    # TODO:: auto() works to differentiate, but it doesn't an int value, only <enum.auto object at ... check that
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


# TODO: add to tests
def main():
    print(Bird.FLAMINGO)
    print(Bird.FLAMINGO.value)
    print(Bird.FLAMINGO.small_flock)
    print(Bird.FLAMINGO.big_flock)
    print(Bird.FLAMINGO.copies)

    print(list(Bird))
    assert str(list(Bird)) == '[F, O, T, D, P, M, N, R]'
    assert len(Bird) == 8

    print(Bird.get_deck())
    assert str(Bird.get_deck()) == '[[F, F, F, F, F, F, F], [O, O, O, O, O, O, O, O, O, O], [T, T, T, T, T, T, T, T, T, T], [D, D, D, D, D, D, D, D, D, D, D, D, D], [P, P, P, P, P, P, P, P, P, P, P, P, P], [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M], [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N], [R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R]]'
    assert len(Bird.get_deck()) == 8
    assert sum(map(len, Bird.get_deck())) == 110


if __name__ == '__main__':
    main()
