import itertools as it
from collections import Counter
from functools import lru_cache


@lru_cache
def dice_permutations(dice_count, players, min_dice=1, max_dice=4, verbose=False):

    if verbose:
        spaces = " " * players
        print(spaces, (dice_count, players))

    if dice_count < players:
        return 0

    if dice_count == 0 and players == 0:
        return 1

    if players == 0 or dice_count < 0:
        return 0

    permutations = 0
    for i in range(min_dice, max_dice + 1):
        permutations += dice_permutations(
            dice_count - i, players - 1, min_dice, max_dice, verbose
        )

    return permutations
