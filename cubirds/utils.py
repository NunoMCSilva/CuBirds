from __future__ import annotations

from random import sample


def shuffle(x):
    # shuffle "not in place"
    return sample(x, len(x))
