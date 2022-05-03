import altair as alt
from altair import datum
import  pandas as pd
import numpy as np

x = np.linspace(-1, 1, num=3)

df = pd.DataFrame({
    'x': x,
    'abs(x)': np.abs(x),
})


# slider = alt.binding_range(min=-1, max=1, step=0.1, name='x:')
# select_x = alt.selection_single(
#     name="x", 
#     fields=['x'],
#     bind=slider, 
#     init={'x': 0.0}
# )

base_chart = alt.Chart(df).encode(
    x=alt.X(
        'x',
        scale=alt.Scale(domain=[-1, 1])
    ),
    y=alt.Y(
        'abs(x)',
        scale=alt.Scale(domain=[-1, 1])
    )
)

line_chart = base_chart.mark_line()

#  .add_selection( 
#     select_x
# ).transform_filter(
#     select_x
# )


chart = line_chart

chart.properties(width="container", height="container").save("../../assets/vega-charts/lorem-ipsum/mad-plot.json")