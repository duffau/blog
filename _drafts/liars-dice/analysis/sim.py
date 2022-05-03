import math
import random
from collections import Counter
from pickle import TRUE

KIND = 6
JOKER = 1
REPS = 100000
SIDES = [1, 2, 3, 4, 5, 6]
N_DICE_INITIAL = 8
N_DICE_PER_PLAYER = 4
DICE_ASSIGNMENT_STRATEGY = "even"

USE_STAIR = True
USE_JOKER = True


def is_stair(face_values: list):
    if min(face_values) == 1:
        return is_unique_values(face_values)
    else:
        return False


def is_unique_values(l):
    s = set()
    for x in l:
        if x in s:
            return False
        s.add(x)
    return True


def roll_dice(n):
    return random.choices(SIDES, k=n)


def n_kinds(face_values, use_stair=True, use_joker=True):
    if use_stair and is_stair(face_values):
        return len(face_values) + 1

    n = sum([fv == KIND for fv in face_values])
    if use_joker:
        n += sum([fv == JOKER for fv in face_values])
    return n


def max_number_of_kinds(players_dice, use_stair=True):
    if use_stair:
        max_kinds = sum([pd + 1 for pd in players_dice])
    else:
        max_kinds = sum(players_dice)

    return max_kinds


def assign_players_dice(n_dice, n_dice_per_player, strategy):
    if strategy == "residual":
        players_dice = [n_dice_per_player] * (n_dice // n_dice_per_player)
        if n_dice % n_dice_per_player:
            players_dice.append(n_dice % n_dice_per_player)
    elif strategy == "even":
        n_players = max(math.ceil(n_dice / n_dice_per_player), 2)
        players_dice = [n_dice_per_player] * n_players
        while sum(players_dice) > n_dice:
            i = players_dice.index(max(players_dice))
            players_dice[i] -= 1
    else:
        raise ValueError(f"strategy: '{strategy}' not defined")
    return players_dice


def remove_one_from_players_dice(players_dice):
    i = players_dice.index(max(players_dice))
    players_dice[i] -= 1
    players_dice = trim_zero_dice_players(players_dice)
    return players_dice


def trim_zero_dice_players(players_dice):
    return [n_dice for n_dice in players_dice if n_dice != 0]


players_dice = assign_players_dice(
    N_DICE_INITIAL, N_DICE_PER_PLAYER, strategy=DICE_ASSIGNMENT_STRATEGY
)
print(f"n initial dice = {N_DICE_INITIAL}")
print(f"n inital players = {len(players_dice)}")
print(f"With dice = {players_dice}")
print(f"With stair rule: {USE_STAIR}")
print(f"With joker rule: {USE_JOKER}")

while sum(players_dice) > 2:
    players_dice = remove_one_from_players_dice(players_dice)
    print(f"With dice = {players_dice}")
    max_kinds = max_number_of_kinds(players_dice, use_stair=USE_STAIR)
    print(f"Max number of kinds = {max_kinds}")

    _n_kinds = []
    for _ in range(REPS):
        n = 0
        for n_dice in players_dice:
            face_values = roll_dice(n_dice)
            n += n_kinds(face_values, use_stair=USE_STAIR, use_joker=USE_JOKER)
        _n_kinds.append(n)

    counter = Counter(_n_kinds)
    total = sum(counter.values())
    count = 0
    for n_kind in range(1, max_kinds + 1):
        count = sum([counter.get(n, 0) for n in range(n_kind, max_kinds + 1)])
        print(
            f"n kinds =  {n_kind}, n = {count:6}, p(at least {n_kind} kinds) = {count/total*100  if total > 0 else None:.2g}%"
        )
