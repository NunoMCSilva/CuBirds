from __future__ import annotations

from abc import ABC
from dataclasses import dataclass


class Move(ABC):
    pass


@dataclass
class Place(Move):
    bird: Bird
    row: int
    side: Side


@dataclass
class Fly(Move):
    bird: Bird


@dataclass  # dataclass is not needed here, but with it there is no need to code __str__ and __repr__
class Buy(Move):
    pass


@dataclass  # dataclass is not needed here, but with it there is no need to code __str__ and __repr__
class Pass(Move):
    pass


# TODO: add to tests
def main():
    from bird import Bird
    from side import Side

    p = Place(Bird.OWL, 3, Side.LEFT)
    f = Fly(Bird.FLAMINGO)
    # TODO: these two might be turned into Singletons, but... is there a need for it?
    b = Buy()
    pa = Pass()
    print(p, f, b, pa)

    # TODO: needed in tests, this is just a language issue I wanted to check
    assert isinstance(p, Move)
    assert isinstance(p, Place)
    assert not isinstance(p, Buy)
    assert not isinstance(pa, Fly)

    print(repr(b))
    print([p, f, b, pa])


if __name__ == '__main__':
    main()
