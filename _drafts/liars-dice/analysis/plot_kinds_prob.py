import altair as alt
import numpy as np
import pandas as pd

source = pd.read_csv("kinds_prob.csv")
source.prob = source.prob * 100

ANNOTATIONS_FONT_SIZE = 9

min_dice = source.dice.min()
max_dice = source.dice.max()
min_kinds = source.kinds.min()
max_kinds = source.kinds.max()


with_joker_radio_button = alt.binding_radio(options=[True, False], name="With Joker:")
select_with_joker = alt.selection_single(
    name="with_joker",
    fields=["with_joker"],
    bind=with_joker_radio_button,
    init={"with_joker": True},
)
with_stair_radio_button = alt.binding_radio(options=[True, False], name="With Ladder:")
select_with_stair = alt.selection_single(
    name="with_stair",
    fields=["with_stair"],
    bind=with_stair_radio_button,
    init={"with_stair": False},
)


base_chart = alt.Chart(source).encode(
    x=alt.X("kinds:O", scale=alt.Scale(domain=np.arange(min_kinds, max_kinds + 1))),
    y=alt.Y("dice:O", scale=alt.Scale(domain=np.arange(min_dice, max_dice + 1))),
    color=alt.X("prob:Q", scale=alt.Scale(domain=[0.0, 100.0])),
)

heatmap = (
    base_chart.mark_rect()
    .add_selection(select_with_joker)
    .transform_filter(select_with_joker)
    .add_selection(select_with_stair)
    .transform_filter(select_with_stair)
)

text = (
    base_chart.mark_text(baseline="middle", fontSize=ANNOTATIONS_FONT_SIZE)
    .encode(
        text="label:Q",
        color=alt.condition(
            alt.datum.label > 50, alt.value("white"), alt.value("black")
        ),
    )
    .transform_calculate(label='format(datum.prob, ".0f")')
    .transform_filter(select_with_joker)
    .transform_filter(select_with_stair)
)


chart = heatmap + text
chart.properties(width="container", height="container").save(
    "../../../assets/vega-charts/liars-dice/kinds-prob-plot.json"
)
chart.properties(width=300, height=300).save(
    "../../../assets/vega-charts/liars-dice/kinds-prob-plot.html"
)
