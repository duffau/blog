import pandas as pd

from liars_dice.kinds_probs import probs

DICE_RANGE = (1, 16)
KIND_RANGE = (1, 20)
DICE_ASSIGNMENT_STRATEGY = "random"
COL_WITH_JOKER = "with_joker"
COL_WITH_STAIR = "with_stair"
SIM_REPS = 10000

VERBOSE = True

# joker_stair_combinations = [
#     (use_joker, use_stair)
#     for use_joker in [True, False]
#     for use_stair in [True, False]
# ]
# prob_tables = []
# for use_joker, use_stair in joker_stair_combinations:
#     print(f"Calculating prob combination use_joker: {use_joker}, use_stair: {use_stair}")
use_joker = True
use_stair = True
_prob_table = probs(
    dice_range=DICE_RANGE,
    kinds_range=KIND_RANGE,
    use_joker=use_joker,
    use_stair=use_stair,
    sim_strategy=DICE_ASSIGNMENT_STRATEGY,
    sim_reps=SIM_REPS,
    verbose=VERBOSE,
)
# _prob_table[COL_WITH_JOKER] = use_joker
# _prob_table[COL_WITH_STAIR] = use_stair
# prob_tables.append(_prob_table)
# prob_table = pd.concat(prob_tables)
# print("prob_table.shape:", prob_table.shape)
# prob_table.to_csv("kinds_prob.csv")
