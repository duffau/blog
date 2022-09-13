import altair as alt
import numpy as np
import pandas as pd

pd.set_option("display.max_rows", None)

source = pd.read_csv("kinds_prob.csv")

# Selecting
source = source[
    ((source.with_joker == False) & (source.with_stair == False))
    | ((source.with_joker == True) & (source.with_stair == False))
    | ((source.with_joker == True) & (source.with_stair == True))
]

source.prob = source.prob * 100
source["rules"] = [
    f"Joker: {with_joker}, Stair: {with_stair}"
    for with_joker, with_stair in zip(source.with_joker, source.with_stair)
]

median_lower = source[source.prob <= 50].groupby(["dice", "rules"]).kinds.min()
median_upper = source[source.prob >= 50].groupby(["dice", "rules"]).kinds.max()

median_lower = median_lower.reset_index()
median_upper = median_upper.reset_index()

median_lower["median_type"] = "lower"
median_upper["median_type"] = "upper"

median = pd.concat([median_lower, median_upper])

median.sort_values(by=["rules", "median_type", "dice"], inplace=True)

median["type"] = [
    f"{rule} {median_type}"
    for rule, median_type in zip(median.rules, median.median_type)
]


print(median)
chart = (
    alt.Chart(median)
    .encode(x="dice:Q", y="kinds:Q", color="type")
    .mark_line(interpolate="linear")
    .configure_range(category={"scheme": "paired"})
)

chart.properties(width=300, height=300).save(
    "../../../assets/vega-charts/liars-dice/kinds-median-plot.html"
)

chart = (
    alt.Chart(median_lower)
    .encode(x="dice:Q", y="kinds:Q", color=alt.Color("rules:N", legend=None))
    .mark_line(interpolate="step-after")
)


labels = (
    alt.Chart(median_lower)
    .mark_text(align="right", dx=-3, dy=8)
    .encode(
        alt.X("dice:Q", aggregate="max"),
        alt.Y("kinds:Q", aggregate="max"),
        alt.Text("rules"),
        alt.Color(
            "rules",
            legend=None,
            scale=alt.Scale(domain=sorted(source["rules"].unique()), type="ordinal"),
        ),
    )
)

chart = alt.layer(chart, labels).resolve_scale(color="independent")


chart.properties(width=300, height=300).save(
    "../../../assets/vega-charts/liars-dice/kinds-median-plot-1.html"
)
