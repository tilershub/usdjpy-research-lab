---
title: "Expectancy: the one number that says whether your trading works"
description: "Expectancy combines win rate and average win/loss into one number per trade. The formula, worked examples in R, and when to trust it."
hub: "performance"
updated: "2026-07-07"
reading_time: 8
order: 2
faq:
  - q: "What is a good expectancy for a trader?"
    a: "Any positive expectancy means the strategy makes money on average per trade before costs; there is no universal threshold beyond that. What matters is that the number is positive after commissions and slippage, measured over a meaningful sample, and large enough relative to its variability that it is unlikely to be luck. A modest positive expectancy executed consistently outperforms a larger one executed erratically."
  - q: "Can a high win rate still produce a losing strategy?"
    a: "Yes, easily. If average losses are large relative to average wins, a high win rate cannot compensate. A strategy winning 70% of the time with 0.3R average winners and 1R losses has an expectancy of minus 0.09R per trade — it loses money on average despite winning most trades. Win rate only has meaning alongside the payoff ratio, which is why expectancy combines both."
  - q: "How many trades do I need before my expectancy is trustworthy?"
    a: "Treat anything under a few dozen trades as noise. Small samples are dominated by variance: a genuinely negative-expectancy approach can look brilliant over 15 trades, and a sound one can look broken. Most traders should want at least 30 to 50 trades of one consistent strategy before drawing tentative conclusions, and meaningfully more before making major decisions like paying for a funded challenge."
  - q: "Why is expectancy measured in R-multiples instead of currency?"
    a: "R-multiples express every result as a multiple of the amount initially risked, which removes account size and position size from the measurement. An expectancy of 0.4R means the strategy earns 0.4 times your per-trade risk on average, whatever that risk is in dollars. This makes results comparable across instruments and account sizes, and connects directly to position sizing: expectancy tells you the edge, sizing decides how much capital rides on it."
related:
  - { title: "Win rate and profit factor", href: "/performance/win-rate-and-profit-factor/" }
  - { title: "The professional trading journal", href: "/performance/trading-journal-guide/" }
  - { title: "Position sizing guide", href: "/risk-management/position-sizing/" }
---

Two traders can both say "my strategy works" and mean completely different things. One wins often; the other wins big. Neither claim, on its own, says anything about profitability. Expectancy is the number that settles it: the average amount a strategy makes or loses per trade, with win rate and payoff size combined into a single figure. It is the closest thing trading has to a bottom line, and it is computed from nothing more than the fields a decent [trading journal](/performance/trading-journal-guide/) already captures.

## The formula

Expectancy per trade is:

**Expectancy = (Win% × Average Win) − (Loss% × Average Loss)**

The professional convention is to express wins and losses in R-multiples — results as a multiple of the amount risked on the trade. A trade risking 1R that hits a target twice as far as the stop is +2R; a full stop-out is −1R. Working in R strips out account size and position size, so the number describes the strategy itself. How much actual capital sits behind each R is a separate decision, covered in the [position sizing guide](/risk-management/position-sizing/).

A positive expectancy means the strategy earns money on average per trade; negative means it loses on average, and no amount of discipline, patience, or capital fixes that — only changing the strategy does.

## Two worked examples

These are hypothetical numbers chosen to illustrate the math, not performance claims.

**Example 1 — losing often, making money.** A trader wins 40% of trades. Winners average +2R; losers average −1R (stops honored, in full).

Expectancy = (0.40 × 2R) − (0.60 × 1R) = 0.80R − 0.60R = **+0.20R per trade**

The trader loses six trades out of every ten and still earns 0.20R per trade on average — over 100 trades, roughly +20R before costs. If each R is 0.5% of the account, that is the engine of a sustainable book, despite a win rate that feels like constant failure.

**Example 2 — winning often, losing money.** A trader wins 70% of trades by taking profits quickly: winners average just +0.3R, while losses run to the full −1R.

Expectancy = (0.70 × 0.3R) − (0.30 × 1R) = 0.21R − 0.30R = **−0.09R per trade**

Seven wins in ten, and the account bleeds. Each loss erases more than three average wins. This profile is common precisely because it feels good day to day — the psychology behind that preference is covered in [win rate and profit factor](/performance/win-rate-and-profit-factor/).

## Expectancy across the win-rate / payoff grid

Expectancy per trade, assuming losses average −1R and winners average the stated R:

| Win rate | 0.5R winners | 1R winners | 1.5R winners | 2R winners | 3R winners |
|---|---|---|---|---|---|
| 30% | −0.55R | −0.40R | −0.25R | −0.10R | +0.20R |
| 40% | −0.40R | −0.20R | 0.00R | +0.20R | +0.60R |
| 50% | −0.25R | 0.00R | +0.25R | +0.50R | +1.00R |
| 60% | −0.10R | +0.20R | +0.50R | +0.80R | +1.40R |
| 70% | +0.05R | +0.40R | +0.75R | +1.10R | +1.75R |

Two things stand out. Profitability lives on a diagonal frontier — you can trade anywhere on it, provided win rate and payoff are honest about each other. And the top-left corner is a trap: high win rates with small winners sit at or below breakeven, before commissions and slippage push them further down.

## The sample-size problem

Expectancy is an average, and averages computed from small samples lie. Over 10 or 15 trades, variance dominates: a coin-flip strategy will regularly produce streaks that look like edge, and a genuinely sound strategy will produce stretches that look broken. Treat any expectancy computed from fewer than a few dozen trades as noise. Thirty to fifty trades of one consistent strategy is a reasonable floor for a first estimate; more is better, and the estimate should be recomputed as the [monthly review](/performance/monthly-trading-review/) adds data.

Two practical cautions. First, the trades must come from the same strategy, traded the same way — mixing setups, or changing rules mid-sample, makes the average meaningless. Second, watch for a single outlier doing all the work: if one +8R trade accounts for the entire positive expectancy, the honest reading is "unproven, with one good day," not "profitable."

## Expectancy as a readiness gate for funded challenges

For funded traders, expectancy has a specific, practical use: it is the cheapest possible test of whether you are ready to pay for an evaluation. A challenge fee buys you the right to demonstrate an edge under drawdown rules. If your journal cannot show a positive expectancy over a meaningful sample *before* you pay, the fee is not buying a demonstration — it is buying a lottery ticket, and the evaluation's loss limits will find the negative expectancy quickly.

A sensible gate looks like this: a positive expectancy in R over at least 30–50 trades of the exact strategy you intend to trade in the evaluation, under the same rules you will face (daily stop, maximum risk per trade), with no single trade responsible for the result. Traders who pass that gate treat the challenge as a formality; traders who skip it are effectively running the sample-size experiment with the fee as tuition. The same logic continues after funding — [managing a funded account](/prop-firms/managing-a-funded-account/) is largely the practice of protecting a known positive expectancy from behavioral interference.

Checking a setup's R-multiple before entry takes seconds with a [risk:reward calculator](/risk-reward-calculator/), and it keeps the inputs to your expectancy honest: a "2R target" that routinely gets cut to 0.8R in practice is a different — and possibly unprofitable — strategy.

## Key takeaways

- Expectancy = (Win% × Avg Win) − (Loss% × Avg Loss), expressed in R-multiples; it is the average result per trade.
- Win rate alone proves nothing: 40% with 2R winners is profitable (+0.20R), while 70% with 0.3R winners loses money (−0.09R).
- Profitability is a frontier of win rate and payoff together — many combinations work, and neither number works alone.
- Distrust expectancy from small samples; a few dozen consistent trades is the minimum before the number means anything.
- For funded traders, a demonstrated positive expectancy is the rational prerequisite for paying a challenge fee, not something to discover afterward.
