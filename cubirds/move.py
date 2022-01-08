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


# dataclass is not needed here, but with it there is no need to code __str__ and __repr__
@dataclass
class Buy(Move):
    pass


# dataclass is not needed here, but with it there is no need to code __str__ and __repr__
@dataclass
class Pass(Move):
    pass
