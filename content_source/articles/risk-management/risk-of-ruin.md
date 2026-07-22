---
title: "Risk of Ruin: The Math That Decides Whether You Survive"
description: "What risk of ruin means for funded traders, how win rate and risk per trade interact, and why a 10% drawdown limit changes the entire calculation."
hub: "risk-management"
updated: "2026-07-07"
reading_time: 8
order: 2
faq:
  - q: "What is risk of ruin in trading?"
    a: "Risk of ruin is the probability that your account equity falls to a level from which you can no longer trade. For a personal account that might mean losing everything; for a funded account it means hitting the firm's maximum drawdown limit, which typically sits around 10%. It is driven by three inputs: your win rate, your average payoff ratio, and the percentage of equity you risk on each trade."
  - q: "Why do funded accounts face ruin at 10% drawdown instead of 100%?"
    a: "A prop firm terminates the account the moment equity breaches its maximum drawdown threshold, usually 8-12% below the starting balance or high-water mark. You never get the chance to trade back from a deep hole the way you could in a personal account. Practically, your entire risk-of-ruin calculation has to be run against a 10% barrier, which makes small per-trade risk far more important."
  - q: "Does a high win rate protect me from ruin?"
    a: "Only partially. A high win rate reduces the frequency of long losing streaks, but it cannot eliminate them, and it says nothing about how deep each streak cuts. A trader with a 60% win rate risking 5% per trade can still breach a 10% drawdown limit with just three consecutive losses, an event that basic probability says will occur regularly over a few hundred trades."
  - q: "What risk per trade keeps risk of ruin near zero on a funded account?"
    a: "Most funded traders operate between 0.25% and 1% per trade. At 0.5%, it takes 21 consecutive losses to breach a 10% drawdown limit, which is effectively outside the realm of plausible streaks for any strategy with a genuine edge. At 2% it takes only six consecutive losses, and at 5% just three, which turns an ordinary cold streak into a terminal event."
related:
  - { title: "Daily Loss Limits", href: "/risk-management/daily-loss-limits/" }
  - { title: "Drawdown Explained", href: "/risk-management/drawdown-explained/" }
  - { title: "Position Sizing Guide", href: "/risk-management/position-sizing/" }
---

Every trading strategy with an edge can still destroy the account that runs it. That is the uncomfortable insight behind risk of ruin: profitability and survival are two different mathematical problems. A system that wins over 10,000 trades can still fail in the first 200 if the risk per trade is large enough to let an ordinary losing streak breach the account's failure point. For funded traders, that failure point is not zero — it is a drawdown limit that usually sits around 10%. This article covers the mechanics of ruin, the way win rate and payoff ratio interact with risk size, and why the compressed drawdown limits of prop firm accounts change the arithmetic so dramatically.

## What risk of ruin actually measures

Risk of ruin is the probability that your equity reaches a level from which trading cannot continue. In the classical gambler's-ruin framework, for a bettor making even-money bets with win probability *p* and loss probability *q*, the probability of eventually losing *N* units of capital is:

**RoR = (q / p)^N** (when p > q)

The formula's structure carries the entire lesson. The base *(q/p)* reflects your edge — it is below 1 whenever you win more often than you lose. The exponent *N* is how many risk units your capital contains between where you are now and the point of ruin. Risking 1% per trade against a 10% barrier gives you roughly ten units; risking 0.5% gives you about twenty. Because *N* sits in the exponent, doubling your number of risk units does not halve your risk of ruin — it *squares* the (sub-1) base's effect. Survival improves exponentially as risk per trade shrinks. Real strategies with uneven payoffs need adjusted versions of the formula, but the exponential relationship holds throughout.

## The three inputs and how they interact

Three variables jointly determine ruin risk, and no single one can be evaluated in isolation:

- **Win rate** sets how often losing streaks occur. With a 50% win rate, any given sequence of seven trades has a 0.5^7 ≈ 0.8% chance of being all losses — small per sequence, but across hundreds of independent opportunities in a trading year, extended streaks become an expectation rather than an anomaly. Preparing for them is covered in depth in our guide to [handling losing streaks](/psychology/handling-losing-streaks/).
- **Payoff ratio** (average win ÷ average loss) determines how quickly equity rebuilds between streaks. A 2:1 payoff lets a 40% win rate survive conditions that would ruin a 55% win rate trading at 1:1.5 against.
- **Risk per trade** determines how deep each streak cuts. This is the only input fully under your control, which is why it does most of the work in any survival plan.

Win rate and payoff trade off against each other; risk per trade multiplies the consequences of both. The [position sizing guide](/risk-management/position-sizing/) covers how to translate a chosen risk percentage into an actual trade size.

## Compound drawdown: the real cost of a losing streak

Losses compound. Ten consecutive losses at 1% risk do not produce a 10% drawdown — they produce 1 − 0.99^10 = 9.56%, because each loss is taken on a slightly smaller balance. That compounding works mildly in your favor, but nowhere near enough to rescue oversized risk. The table below uses exact compound arithmetic against the barrier that matters for funded traders — a 10% maximum drawdown.

| Risk per trade | Drawdown after 10 straight losses | Consecutive losses to breach 10% | Qualitative ruin risk (funded account) |
|---|---|---|---|
| 0.5% | 4.89% | 21 | Minimal — a 21-loss streak is implausible for any strategy with a real edge |
| 1% | 9.56% | 11 | Low — survivable, but an 11-loss streak is within reach of a bad month |
| 2% | 18.29% | 6 | Elevated — six straight losses is an ordinary cold streak, not an outlier |
| 5% | 40.13% | 3 | Near-certain over time — three consecutive losses will happen, repeatedly |

Read the right-hand columns together. At 0.5% risk, the account's failure point sits behind a wall of 21 consecutive losses. At 5%, the same account is three losses from termination at all times — and for a coin-flip win rate, a three-loss streak beginning at any given trade has a probability of 12.5%. Over a hundred trades, ruin stops being a risk and becomes a schedule. You can model your own numbers with the [drawdown calculator](/tools/drawdown-calculator/).

## Why funded accounts redefine "ruin"

In a personal account, ruin technically means equity approaching zero, and a disciplined trader can theoretically trade smaller and smaller during a drawdown, stretching survival. A funded account removes that option entirely. The firm's maximum drawdown rule — typically 8-12%, frequently trailing from a high-water mark — is a hard termination line. Breach it once, even intraday on a floating loss at some firms, and the account is gone along with the evaluation fee and the time invested.

This compresses the entire risk-of-ruin problem into one-tenth of its normal space. Every formula stays the same; only *N*, the number of risk units between you and ruin, shrinks by a factor of ten. A 2% risk per trade that would be merely aggressive in a personal account becomes structurally reckless against a 10% barrier. This is the quantitative reason the [risk management framework](/risk-management/) on this site anchors funded traders at conservative per-trade risk, and why the firms' own rules — detailed in our [prop firm rules guide](/prop-firms/prop-firm-rules-explained/) — are best treated as outer fences rather than operating targets.

## Practical implications

The math converts directly into operating decisions:

1. **Choose risk per trade from the drawdown limit backward, not from profit targets forward.** Decide how many consecutive losses your account must survive — 15 to 20 is a defensible standard — and divide the drawdown limit accordingly.
2. **Do not raise risk during drawdowns.** Increasing size to "get it back" shrinks *N* precisely when streak risk is already elevated. That is the ruin formula's worst case, and it is also the psychological failure mode covered in [revenge trading](/psychology/revenge-trading/).
3. **Treat win rate estimates skeptically.** Backtest win rates degrade live. Building your ruin math on a 65% win rate that turns out to be 52% invalidates every downstream number, so size as if your edge were thinner than measured.
4. **Layer a daily circuit breaker on top.** Per-trade risk controls the depth of each cut; a [daily loss limit](/risk-management/daily-loss-limits/) controls how many cuts you can take in one impaired session.

## Key takeaways

- Risk of ruin is the probability of hitting a level where trading must stop — for funded traders, that level is the firm's ~10% drawdown limit, not zero.
- Survival improves exponentially as risk per trade falls, because risk units appear in the exponent of the ruin formula.
- Exact compound math: 10 straight losses produce a 4.89% drawdown at 0.5% risk, 9.56% at 1%, 18.29% at 2%, and 40.13% at 5%.
- At 5% risk per trade, three consecutive losses breach a 10% funded drawdown limit — an event ordinary probability guarantees will recur.
- Size from the drawdown limit backward: decide how long a losing streak you must survive, then let that number set your risk per trade.
