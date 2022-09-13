import math

import altair as alt
import pandas as pd

N_SIDES = 6
DICE_PER_PLAYER = 5


def dice_permutations(n_dice, n_sides):
    return n_sides ** n_dice


def stair_permutations(n_dice, n_sides):
    assert n_dice <= n_sides
    return math.factorial(n_dice)


n_dice = list(range(1, DICE_PER_PLAYER + 1))
probs = []

for _n_dice in n_dice:
    _stair_permutations = stair_permutations(_n_dice, N_SIDES)
    _total_permutations = dice_permutations(_n_dice, N_SIDES)
    _prob = _stair_permutations / _total_permutations
    print(
        f"n_dice: {n_dice}, total_permutations: {_total_permutations}, stair_permutations: {_stair_permutations}, stair probability: {_prob*100:.1f}%"
    )
    probs.append(_prob)

source = pd.DataFrame(data={"dice": n_dice, "stair probability": probs})

chart = alt.Chart(source).mark_bar().encode(x="dice:N", y="stair probability:Q")

chart.properties(width="container", height="container").save(
    "../../../assets/vega-charts/liars-dice/stair-prob-plot.json"
)
