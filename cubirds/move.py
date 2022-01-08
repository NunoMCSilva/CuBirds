from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto

from bird import Bird   # TODO: not really necessary, but PyCharm keeps warning me about it's "lack"


# Side = Enum('Side', 'LEFT RIGHT')
class Side(Enum):
    LEFT = auto()
    RIGHT = auto()

    def __repr__(self):
        return self.name.capitalize()


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


# dataclass is not needed here, but with it there is no need to code __str__ and __repr__
@dataclass
class Buy(Move):
    pass


# dataclass is not needed here, but with it there is no need to code __str__ and __repr__
@dataclass
class Pass(Move):
    pass
