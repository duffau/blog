import numpy as np

import liars_dice.kinds_probs as kp


def test_sim_and_calc_parity():
    use_stair = False
    use_joker = False
    dice_range = [2, 12]
    kinds_range = [1, 12]
    sim_prob_table = kp.simulate_probs(
        dice_range=dice_range,
        kinds_range=kinds_range,
        use_stair=use_stair,
        use_joker=use_joker,
    )
    calc_prob_table = kp.calculate_probs(
        dice_range=dice_range, kinds_range=kinds_range, use_joker=use_joker
    )
    np.allclose(sim_prob_table, calc_prob_table)