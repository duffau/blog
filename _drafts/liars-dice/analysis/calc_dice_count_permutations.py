import pandas as pd

from liars_dice.dice_count_permutations import dice_permutations

min_dice = 1
max_dice = 4
min_players = 2
max_players = 5

data = []
for players in range(min_players, max_players + 1):
    print("")
    for dice_count in range(1, players * max_dice + 1):
        perm = dice_permutations(
            dice_count, players, min_dice=min_dice, max_dice=max_dice
        )
        record = {"players": players, "dice": dice_count, "permutations": perm}
        data.append(record)
        print(
            f"players: {players}, max dice per player: {max_dice}, dice count: {dice_count}, permutations: {perm}"
        )

pd.DataFrame(data=data).to_pickle("dice_count_permutations.pickle")
