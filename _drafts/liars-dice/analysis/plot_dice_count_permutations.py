import altair as alt
import pandas as pd

source = pd.read_pickle("dice_count_permutations.pickle")

highlight = alt.selection(
    type="single",
    on="mouseover",
    fields=["dice", "players"],
    nearest=False,
    empty="none",
)


bars = (
    alt.Chart(source)
    .mark_bar()
    .encode(
        x=alt.X("sum(permutations):Q", stack="zero"),
        y=alt.Y("dice:N"),
        color=alt.Color("players:N"),
        opacity=alt.condition(highlight, alt.value(0.5), alt.value(1)),
    )
    .add_selection(highlight)
)

inside_text = (
    alt.Chart(source)
    .mark_text(dx=-15, color="white")
    .encode(
        x=alt.X("sum(permutations):Q", stack="zero"),
        y=alt.Y("dice:N"),
        detail="players:N",
        text=alt.Text("sum(permutations):Q"),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0)),
    )
)

chart = bars + inside_text

chart.properties().save(
    "../../../assets/vega-charts/liars-dice/dice-count-permutations-plot.json"
)

chart.properties().save(
    "../../../assets/vega-charts/liars-dice/dice-count-permutations-plot.html"
)
