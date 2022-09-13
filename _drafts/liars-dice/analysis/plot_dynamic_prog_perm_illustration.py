from cProfile import label

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

from liars_dice.dice_count_permutations import dice_permutations

PLOT_PATH = (
    "../../../assets/img/liars-dice/dynamic-programming-dice-count-permutations.png"
)

# dice_permutations(5, 4, verbose=True)

# (dice_count, players)
# dice_permutations(dice_count - i, players - 1, min_dice, max_dice)


TAB10_BLUE = "#4c78a8"
TAB10_ORANGE = "#f58418"
TAB10_RED = "#e45756"
TAB10_TURQUOISE = "#72b7b2"
TAB10_GREEN = "#54a24b"
TAB10_YELLOW = "#eeca3b"
TAB10_PURPLE = "#b279a2"
TAB10_PINK = "#fe9ea6"
TAB10_BROWN = "#9d755d"
TAB10_GREY = "#bab0ac"

COLORS = [
    TAB10_BLUE,
    TAB10_ORANGE,
    TAB10_RED,
    TAB10_TURQUOISE,
    TAB10_GREEN,
    TAB10_YELLOW,
    TAB10_PURPLE,
    TAB10_PINK,
    TAB10_BROWN,
    TAB10_GREY,
]

G = nx.Graph()
G.add_nodes_from(
    [
        ((5, 4), {"color": COLORS[0]}),
        ((4, 3), {"color": COLORS[1]}),
        ((3, 3), {"color": COLORS[1]}),
        ((2, 3), {"color": COLORS[1]}),
        ((1, 3), {"color": COLORS[1]}),
        ((3, 2), {"color": COLORS[2]}),
        ((2, 2), {"color": COLORS[2]}),
        ((1, 2), {"color": COLORS[2]}),
        ((2, 1), {"color": COLORS[3]}),
        ((1, 1), {"color": COLORS[3]}),
    ]
)

edges = [
    ((5, 4), (4, 3)),
    ((5, 4), (3, 3)),
    ((5, 4), (2, 3)),
    ((5, 4), (1, 3)),
    ((4, 3), (3, 2)),
    ((4, 3), (2, 2)),
    ((4, 3), (1, 2)),
    ((3, 2), (2, 1)),
    ((3, 2), (1, 1)),
]

G.add_edges_from(edges)

edge_labels = {(n1, n2): "+" for n1, n2 in G.edges}

color_map = [G.nodes[node]["color"] for node in G.nodes]
pos = graphviz_layout(G, prog="dot")
# nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=1200)
nx.draw_networkx(G, pos=pos, with_labels=True, node_color=color_map, node_size=1200)
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    bbox=dict(boxstyle="circle", facecolor="white", pad=0.1),
    rotate=False,
)
plt.tight_layout()
plt.savefig(PLOT_PATH)
