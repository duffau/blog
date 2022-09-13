import math
import random
from collections import Counter
from typing import Iterable, List, Tuple

import numpy as np
import pandas as pd
import scipy.stats as ss
from tqdm import tqdm

SIDES = [1, 2, 3, 4, 5, 6]
KIND = 6
JOKER_VALUE = 1
DICE_PER_PLAYER = 4

COL_DICE = "dice"
COL_KINDS = "kinds"
COL_PROB = "prob"
COLUMNS = [COL_DICE, COL_KINDS, COL_PROB]
STRATEGY_EVEN = "even"
STRATEGY_SINGLE_LOSER = "single loser"
STRATEGY_RANDOM = "random"


def probs(
    dice_range: Tuple[int, int],
    kinds_range: Tuple[int, int],
    use_joker: bool,
    use_stair: bool,
    sim_strategy: str = STRATEGY_EVEN,
    dice_per_player: str = DICE_PER_PLAYER,
    sides: int = SIDES,
    sim_reps: int = 10000,
    verbose: bool = True,
) -> pd.DataFrame:
    if use_stair:
        prob_table = simulate_probs(
            dice_range,
            kinds_range,
            use_joker,
            use_stair,
            dice_per_player,
            sides=sides,
            reps=sim_reps,
            dice_assigment_strategy=sim_strategy,
            verbose=verbose,
        )
    else:
        prob_table = calculate_probs(
            dice_range, kinds_range, use_joker, sides, verbose=verbose
        )
    return prob_table


def calculate_probs(
    dice_range, kinds_range, use_joker, sides=6, verbose=False
) -> pd.DataFrame:
    if verbose:
        print(f"Calculating probabilites:")
        print(f"With dice range: {dice_range}")
        print(f"With kinds range: {kinds_range}")
        print(f"With joker rule: {use_joker}")

    dice = [i for i in range(dice_range[0], (dice_range[1] + 1))]
    if use_joker:
        success_prob = 2 / len(sides)
    else:
        success_prob = 1 / len(sides)

    kinds = [i for i in range(kinds_range[0], kinds_range[1] + 1)]
    dice, kinds = np.meshgrid(dice, kinds)
    dice, kinds = np.ravel(dice), np.ravel(kinds)
    dice, kinds = filter_possible_dice_kind_combinations(dice, kinds)
    prob = 1 - ss.binom.cdf(kinds - 1, dice, p=success_prob)
    data = {
        COL_DICE: dice,
        COL_KINDS: kinds,
        COL_PROB: prob,
    }
    return pd.DataFrame(data, columns=COLUMNS)


def filter_possible_dice_kind_combinations(dice, kinds):
    return dice[kinds <= dice], kinds[kinds <= dice]


def simulate_probs(
    dice_range,
    kinds_range,
    use_joker,
    use_stair,
    dice_per_player=DICE_PER_PLAYER,
    sides=SIDES,
    reps=10000,
    dice_assigment_strategy=STRATEGY_EVEN,
    inner_outer_rep_ratio=0.1,
    verbose=False,
) -> pd.DataFrame:
    print("Simulating probabilities ...")
    if verbose:
        print(f"With stair rule: {use_stair}")
        print(f"With joker rule: {use_joker}")
    min_dice, max_dice = dice_range
    min_kinds, max_kinds = kinds_range

    inner_reps, outer_reps = (
        int(reps / (1 + inner_outer_rep_ratio)),
        int(reps / (1 + 1 / inner_outer_rep_ratio)),
    )
    prob_table = []
    n_kinds, n_dice = [], []
    for _ in tqdm(range(outer_reps)):
        players_dice = assign_players_dice(
            max_dice, dice_per_player, strategy=dice_assigment_strategy
        )
        if verbose:
            print(f"n initial dice = {max_dice}")
            print(f"n inital players = {len(players_dice)}")
            print(f"With dice = {players_dice}")
        while sum(players_dice) >= min_dice and len(players_dice) > 1:
            _max_possible_kinds = max_possible_kinds(players_dice, use_stair=use_stair)
            if verbose:
                print(f"With dice = {players_dice}")
                print(f"Max number of possible kinds = {_max_possible_kinds}")

            _n_kinds = simulate_kinds(
                players_dice, inner_reps, sides, use_stair, use_joker
            )
            _n_dice = [sum(players_dice)] * inner_reps
            n_kinds.extend(_n_kinds)
            n_dice.extend(_n_dice)
            players_dice = remove_one_from_wining_players_dice(
                players_dice, strategy=dice_assigment_strategy
            )

    prob_table = calc_prob_table(
        n_kinds, n_dice, min_kinds, _max_possible_kinds, verbose
    )
    prob_table = pd.DataFrame(data=prob_table, columns=COLUMNS)
    prob_table = prob_table[
        (prob_table.kinds >= min_kinds) & (prob_table.kinds <= max_kinds)
    ]
    return prob_table


def simulate_kinds(players_dice, reps, sides, use_stair, use_joker) -> List:
    n_dice = sum(players_dice)
    _n_kinds = []
    for _ in range(reps):
        n = 0
        for n_dice in players_dice:
            face_values = roll_dice(n_dice, sides)
            n += n_kinds(face_values, use_stair=use_stair, use_joker=use_joker)
        _n_kinds.append(n)
    return _n_kinds


def calc_prob_table(
    n_kinds: List[int], n_dice: List[int], min_kinds, max_kinds, verbose
) -> List[Tuple]:
    if len(n_kinds) != len(n_dice):
        raise ValueError(
            f"Length of n_kinds and n_dice must match. len(n_kinds) = {len(n_kinds)}, len(n_dice) = {len(n_dice)}"
        )
    prob_table = []
    unique_n_dice_values = sorted(list(set(n_dice)))
    for _n_dice in unique_n_dice_values:
        _n_kinds = [nk for nk, nd in zip(n_kinds, n_dice) if nd == _n_dice]
        _prob_table = calc_single_prob_table(
            _n_kinds, _n_dice, min_kinds, max_kinds, verbose
        )
        prob_table.extend(_prob_table)
    return prob_table


def calc_single_prob_table(
    n_kinds: List[int], n_dice: int, min_kinds, max_kinds, verbose
):
    _prob_table = []
    counter = Counter(n_kinds)
    total = sum(counter.values())
    for n_kind in range(min_kinds, max_kinds + 1):
        count = sum([counter.get(n, 0) for n in range(n_kind, max_kinds + 1)])
        prob = count / total if total > 0 else None
        if verbose:
            print(
                f"n kinds =  {n_kind}, n = {count:6}, p(at least {n_kind} kinds) = {prob*100:.2g}%"
            )
        row = (n_dice, n_kind, prob)
        _prob_table.append(row)
    return _prob_table


def is_stair(face_values: List) -> bool:
    if min(face_values) == 1:
        return is_unique_values(face_values)
    else:
        return False


def is_unique_values(l: Iterable) -> bool:
    s = set()
    for x in l:
        if x in s:
            return False
        s.add(x)
    return True


def roll_dice(n, sides) -> int:
    return random.choices(sides, k=n)


def n_kinds(
    face_values: List[int], use_stair=True, use_joker=True, joker_value=JOKER_VALUE
) -> int:
    if use_stair and is_stair(face_values):
        return len(face_values) + 1

    n = sum([fv == KIND for fv in face_values])
    if use_joker:
        n += sum([fv == joker_value for fv in face_values])
    return n


def max_possible_kinds(players_dice: List[int], use_stair=True) -> int:
    if use_stair:
        max_kinds = sum([pd + 1 for pd in players_dice])
    else:
        max_kinds = sum(players_dice)

    return max_kinds


def assign_players_dice(
    n_dice: int, n_dice_per_player: int, strategy: str
) -> List[int]:
    if strategy == STRATEGY_SINGLE_LOSER:
        players_dice = [n_dice_per_player] * (n_dice // n_dice_per_player)
        if n_dice % n_dice_per_player:
            players_dice.append(n_dice % n_dice_per_player)
    elif strategy == STRATEGY_EVEN:
        n_players = max(math.ceil(n_dice / n_dice_per_player), 2)
        players_dice = [n_dice_per_player] * n_players
        while sum(players_dice) > n_dice:
            i = players_dice.index(max(players_dice))
            players_dice[i] -= 1
    elif strategy == STRATEGY_RANDOM:
        n_players = max(math.ceil(n_dice / n_dice_per_player), 2)
        players_dice = [n_dice_per_player] * n_players
        while sum(players_dice) > n_dice:
            i = random.randrange(0, len(players_dice))
            players_dice[i] -= 1
    else:
        raise ValueError(f"strategy: '{strategy}' not defined")
    return players_dice


def remove_one_from_wining_players_dice(players_dice: List[int], strategy: str):
    if strategy == STRATEGY_EVEN:
        losing_player = players_dice.index(min(players_dice))
    elif strategy == STRATEGY_SINGLE_LOSER:
        losing_player = players_dice.index(max(players_dice))
    elif strategy == STRATEGY_RANDOM:
        losing_player = random.randrange(0, len(players_dice))
    else:
        raise ValueError(f"strategy: '{strategy}' not defined")
    for i in range(len(players_dice)):
        if i != losing_player:
            players_dice[i] -= 1
    players_dice = trim_zero_dice_players(players_dice)
    return players_dice


def trim_zero_dice_players(players_dice: List[int]) -> List[int]:
    return [n_dice for n_dice in players_dice if n_dice != 0]
