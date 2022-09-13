---
layout: post
title:  "Liar's Dice"
date:   2022-05-04
---

# Intro

# No fancy rules

$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}
$$


# The ladder


<div style="text-align: center;">
    <div id="stair-prob" style="width: 500px; height: 400px; display: inline-block;"></div>
</div>

<script type="text/javascript">
  var spec = "{{ site.baseurl }}/assets/vega-charts/liars-dice/stair-prob-plot.json";
  vegaEmbed('#stair-prob', spec).then(function(result) {}).catch(console.error);
</script>

<div style="text-align: center;">
    <div id="dice-count-permutations" style="width: 500px; height: 400px; display: inline-block;"></div>
</div>

<script type="text/javascript">
  var spec = "{{ site.baseurl }}/assets/vega-charts/liars-dice/dice-count-permutations-plot.json";
  vegaEmbed('#dice-count-permutations', spec).then(function(result) {}).catch(console.error);
</script>


## Side note: On computing dice count permutations


![Dynamic Programming solution to dice count permutations]({{ site.baseurl }}/assets/img/liars-dice/dynamic-programming-dice-count-permutations.png)

```python
from functools import lru_cache

@lru_cache
def dice_permutations(dice_count, players):
    min_dice = 1
    max_dice = 4

    if dice_count < players:
        return 0

    if dice_count == 0 and players == 0:
        return 1

    if players == 0 or dice_count < 0:
        return 0

    permutations = 0
    for i in range(min_dice, max_dice + 1):
        permutations += dice_permutations(dice_count - i, players - 1)

    return permutations
```


<div style="text-align: center;">
    <div id="liars-dice-prob" style="width: 500px; height: 400px; display: inline-block;"></div>
</div>

<script type="text/javascript">
  var spec = "{{ site.baseurl }}/assets/vega-charts/liars-dice/prob-plot.json";
  vegaEmbed('#liars-dice-prob', spec).then(function(result) {}).catch(console.error);
</script>



# A rule of thumb