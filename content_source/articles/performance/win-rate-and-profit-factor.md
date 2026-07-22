---
title: "Win rate and profit factor: reading the two numbers together"
description: "Win rate means nothing without the payoff ratio. How profit factor ties them together, break-even math by R:R, and the hidden risk of high win rates."
hub: "performance"
updated: "2026-07-07"
reading_time: 8
order: 3
faq:
  - q: "What is a good profit factor?"
    a: "Any value above 1.0 means gross profits exceeded gross losses over the period measured. Sustained values well above 1.0, held across many trades and different market conditions, indicate a robust edge, while values hovering just above 1.0 can be erased by costs and variance. Be skeptical of very high profit factors from short periods — they usually reflect a small sample or one favorable stretch rather than a durable edge."
  - q: "Is a 50% win rate good or bad?"
    a: "By itself, neither — it depends entirely on the payoff ratio. At 50% wins, a strategy averaging 1.5R winners against 1R losses is solidly profitable, while one averaging 0.8R winners loses money. The break-even win rate is determined by the reward-to-risk ratio: 50% at 1:1, 33.3% at 1:2, 25% at 1:3. Judge the pair, never the win rate alone."
  - q: "Why do high win-rate strategies fail so often?"
    a: "Because a high win rate is often purchased by accepting rare, large losses — cutting winners early while letting losers run, or selling risk that pays small premiums until it doesn't. The equity curve looks smooth for months, then a single tail event returns years of small gains. The frequent wins also build overconfidence, so size tends to grow at exactly the wrong time. The danger is hidden in the trades that haven't happened yet."
  - q: "How are profit factor and expectancy related?"
    a: "They describe the same underlying performance from different angles. Expectancy is the average result per trade in R-multiples; profit factor is the ratio of total gross profit to total gross loss. A positive expectancy always corresponds to a profit factor above 1.0 and vice versa. Expectancy is more useful for projecting outcomes per trade, while profit factor gives a quick, scale-free health check of a track record."
related:
  - { title: "Expectancy explained", href: "/performance/expectancy-explained/" }
  - { title: "The monthly trading review", href: "/performance/monthly-trading-review/" }
  - { title: "Risk:Reward calculator", href: "/risk-reward-calculator/" }
---

"I win 68% of my trades" sounds like a track record. It is actually half of one, and the missing half decides everything. A 68% win rate with small winners and full-size losers is a slow way to lose money; a 35% win rate with large winners can be an excellent business. Win rate and payoff ratio are two halves of a single statement about edge, and profit factor is the number that forces them to be read together.

## Definitions, precisely

**Win rate** is the percentage of closed trades that were profitable. It measures frequency of success and nothing else — not magnitude, not risk, not profitability.

**Payoff ratio** (average win ÷ average loss) measures magnitude: how large the typical winner is relative to the typical loser. In R-multiple terms, a trader whose winners average +1.8R against −1R losers has a payoff ratio of 1.8.

**Profit factor** is gross profit divided by gross loss over a period: the sum of all winning trades divided by the absolute sum of all losing trades. A profit factor of 1.0 is exact breakeven. Above 1.0, the strategy made money over the period; below it, it lost. Qualitatively: anything above 1.0 is profitable, values only slightly above 1.0 are fragile once commissions, slippage, and ordinary variance are accounted for, and sustained values well above 1.0 — held across many trades and different conditions — are the signature of a genuine edge. A very high profit factor over a short window deserves suspicion rather than celebration; it usually means a small sample.

Profit factor and [expectancy](/performance/expectancy-explained/) are two views of the same performance: any positive expectancy implies a profit factor above 1.0, and both are computed from the same journal columns.

## The break-even frontier: pure arithmetic

For a strategy where every loss is −1R and every win is +NR, the win rate needed to break even is 1 ÷ (1 + N). This is not an opinion or a market observation — it is arithmetic.

| Reward-to-risk per trade | Break-even win rate | Win 5 points higher → expectancy |
|---|---|---|
| 1:1 (1R winners) | 50.0% | 55% → +0.10R per trade |
| 1:1.5 | 40.0% | 45% → +0.125R per trade |
| 1:2 (2R winners) | 33.3% | 38.3% → +0.15R per trade |
| 1:3 (3R winners) | 25.0% | 30% → +0.20R per trade |
| 1:0.5 (0.5R winners) | 66.7% | 71.7% → +0.075R per trade |

Read the last row carefully. A trader taking half-R winners must win two trades in three just to stand still — before costs. Meanwhile a trader holding for 2R winners can be wrong two times in three and still break even. Every point of win rate above the frontier is edge; every point below it is a subsidy paid to the market. Checking where a setup sits on this frontier before entry is exactly what the [risk:reward calculator](/risk-reward-calculator/) is for.

The frontier also explains a common self-deception: moving stops wider and targets closer *will* raise your win rate, and it will do so by sliding you down the frontier toward a higher break-even requirement. You have not improved the strategy; you have repriced it.

## Why high win rates feel better — and what they can hide

Human preference is not neutral between these profiles. A 70% win-rate strategy delivers frequent small confirmations; a 35% win-rate strategy delivers long losing streaks even when it is working perfectly. Most traders, left to instinct, drift toward the high win-rate profile because it is emotionally cheaper — the discomfort of streaks is real, and it is exactly the pressure examined in [handling losing streaks](/psychology/handling-losing-streaks/).

The danger is that a high win rate can be *manufactured* by accepting tail risk. Cut every winner at +0.3R and give every loser room to "come back," and the win rate climbs while the payoff ratio collapses. The equity curve looks smooth — right up to the trade that doesn't come back. Strategies with this shape often show months of steady gains and then a single loss that erases them, which is why a smooth curve with a very high win rate should prompt a specific question: *what is the largest loss this approach permits, and how often has it merely not happened yet?*

For funded traders the asymmetry is sharper still. Evaluation and funded accounts carry daily and maximum drawdown limits, so the rare large loss doesn't just dent the curve — it can end the account. A modest win rate with controlled −1R losers is structurally safer under those rules than a high win rate with occasional −4R events, even when both have identical expectancy on paper. The [risk management hub](/risk-management/) covers the loss-capping rules; the point here is that win rate tells you nothing about whether those rules are being honored.

## Using the pair in practice

In a [monthly review](/performance/monthly-trading-review/), read the three numbers as a set, in this order:

1. **Profit factor** answers *did the period make money, robustly?* Above 1.0 and stable across months is what you want; hovering at 1.0 means the edge and the costs are fighting to a draw.
2. **Payoff ratio vs. win rate** answers *where does the edge come from?* Locate yourself on the frontier table. Comfortably above the break-even line for your R:R, or living on it?
3. **Trend across months** answers *is the profile drifting?* A rising win rate with a falling payoff ratio is usually not improvement — it is winners being cut earlier, and the frontier math says it can be a net loss even as the win percentage climbs.

None of this requires software beyond the R-multiples and outcomes a disciplined [trading journal](/performance/trading-journal-guide/) already contains.

## Key takeaways

- Win rate measures frequency, payoff ratio measures magnitude; neither means anything alone, and profitability requires reading the pair.
- Profit factor = gross profit ÷ gross loss: above 1.0 is profitable, barely above 1.0 is fragile after costs, and sustained values well above 1.0 indicate real edge.
- Break-even win rate is pure math: 50% at 1:1, 33.3% at 1:2, 25% at 1:3 — every trade sits somewhere on this frontier.
- A rising win rate achieved by shrinking winners is often disguised deterioration, not improvement.
- High win-rate profiles feel better but can conceal tail risk — a critical liability under funded-account drawdown rules, where one oversized loss ends the account.
