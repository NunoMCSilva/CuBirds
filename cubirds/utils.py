from __future__ import annotations

from random import sample


def shuffle(x):
    # shuffle "not in place"
    return sample(x, len(x))


def count_adjacent(x, value, start=0):
    count = 0

    for elem in x[start:]:
        if elem != value:
            break
        count += 1

    return count
