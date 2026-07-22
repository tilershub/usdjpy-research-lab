---
title: "Drawdown Explained: Absolute, Trailing, Daily, and the Cost of Recovery"
description: "Every drawdown type funded traders face — absolute, trailing, daily, maximum — with worked examples, recovery math, and the high-water-mark trap."
hub: "risk-management"
updated: "2026-07-07"
reading_time: 9
order: 4
faq:
  - q: "What is the difference between absolute and trailing drawdown?"
    a: "Absolute drawdown is measured from your starting balance, so the failure floor never moves: a $100,000 account with a 10% absolute limit can always fall to $90,000 and no lower. Trailing drawdown is measured from your highest equity point, so the floor rises as you profit. After growing that same account to $105,000, a 10% trailing floor sits at $94,500 — profits you have not locked in raise the level at which you fail."
  - q: "Why does a 50% drawdown require a 100% gain to recover?"
    a: "Because gains are earned on the smaller, post-loss balance. If $100,000 falls to $50,000, doubling that $50,000 is what it takes to get back to $100,000. The formula is required gain = drawdown / (1 - drawdown), and it accelerates: 10% down needs 11.1% back, 20% needs 25%, and 50% needs 100%. This asymmetry is the core mathematical argument for keeping drawdowns shallow in the first place."
  - q: "What is a high-water mark and why does it matter on funded accounts?"
    a: "The high-water mark is the highest equity level your account has reached, and trailing drawdown rules measure your failure floor from it. On many funded accounts the mark updates on unrealized profits too, so a winning trade you let run raises your floor even if you never close it in profit. That means you can breach the account while sitting above your original starting balance."
  - q: "How should I manage drawdown proactively rather than reactively?"
    a: "Set graduated responses before you need them: a level where you cut position size (often after roughly a third of your allowed drawdown is used), a level where you stop and review, and a personal maximum well inside the firm's. Reducing size during drawdowns slows the approach to the floor and lowers the recovery burden, while raising size to recover faster is the single most reliable way to convert a drawdown into a breach."
related:
  - { title: "Risk of Ruin", href: "/risk-management/risk-of-ruin/" }
  - { title: "Daily Loss Limits", href: "/risk-management/daily-loss-limits/" }
  - { title: "Drawdown Calculator", href: "/tools/drawdown-calculator/" }
---

Drawdown is the only trading statistic that can end your career while your strategy is working. Two traders can run the same system with the same long-run expectancy, and the one who misunderstands how their account measures drawdown — from the starting balance, from a high-water mark, from this morning's snapshot — can fail while the other passes. Funded accounts have made this a definitional problem as much as a performance problem: before you can manage drawdown, you have to know precisely which drawdown you are being measured against.

## The four drawdowns that matter

**Absolute drawdown** measures decline from the starting balance, and the floor never moves. A $100,000 account with a 10% absolute (often called "static") limit fails at $90,000 — today, and equally after the account has grown to $115,000. This is the most forgiving structure, because profits build permanent cushion.

**Relative (trailing) drawdown** measures decline from the highest equity the account has reached — the high-water mark. The floor rises as you profit and never falls. Same $100,000 account with a 5% trailing limit: after equity peaks at $108,000, the floor sits at $102,600 — *above* the balance you started with. Fall back to $102,500 and the account is breached while showing a 2.5% gain. Trailing rules convert unbanked profit into raised stakes.

**Daily drawdown** measures decline from a start-of-day snapshot and resets at each rollover — typically a 4-5% floor. It operates on a one-session clock and is the subject of its own article on [daily loss limits](/risk-management/daily-loss-limits/).

**Maximum drawdown** is the analytical statistic: the largest peak-to-trough decline over the account's whole history, the number that summarizes the worst stretch your strategy has actually produced.

## Worked examples

Take one equity path and measure it four ways. A $100,000 account trades for three weeks: rises to $104,000, falls to $97,500, recovers to $106,000, then falls to $100,700.

| Measure | Calculation | Result |
|---|---|---|
| Absolute drawdown (worst) | ($100,000 − $97,500) ÷ $100,000 | 2.50% |
| Trailing drawdown at the $97,500 low | ($104,000 − $97,500) ÷ $104,000 | 6.25% |
| Trailing drawdown at the $100,700 low | ($106,000 − $100,700) ÷ $106,000 | 5.00% |
| Maximum drawdown (peak-to-trough) | ($104,000 − $97,500) ÷ $104,000 | 6.25% |

The same trading produced a 2.5% drawdown under an absolute rule and a 6.25% drawdown under a trailing rule. Against a 6% trailing limit, this account is breached; against a 10% absolute limit, it was never in danger. Neither the strategy nor the execution differed — only the measurement. You can reproduce these calculations for your own equity path with the [drawdown calculator](/tools/drawdown-calculator/).

## The asymmetry of recovery

Percentages are not symmetric around zero. A loss shrinks the base on which the recovery must be earned, so the gain required to break even is always larger than the drawdown that caused it. The exact relationship is **required gain = drawdown ÷ (1 − drawdown)**:

| Drawdown | Gain required to break even |
|---|---|
| 5% | 5.26% |
| 10% | 11.11% |
| 15% | 17.65% |
| 20% | 25.00% |
| 30% | 42.86% |
| 50% | 100.00% |

The curve is gentle at first and then brutal: the first 10% of drawdown adds about one extra point to the recovery bill, while going from 30% to 50% down raises the bill from 43% to 100%. Shallow drawdowns are cheap to repair; deep ones structurally change what your strategy must achieve. This is also why the per-trade risk levels analyzed in [risk of ruin](/risk-management/risk-of-ruin/) matter so much — small risk per trade is what keeps you on the flat part of this curve, where recovery is a routine cost rather than a career project.

## Trailing drawdown traps on funded accounts

Trailing rules produce failure modes that surprise traders coming from personal accounts, because the high-water mark can move against you in ways that feel invisible.

**The unrealized-profit trap.** At many firms the high-water mark updates on *equity*, including open floating profit. Suppose your $100,000 account (5% trailing, $5,000) rides a winner to $104,000 of equity without closing it. The floor rises to $99,000. The trade reverses and you exit at $100,500, then lose $1,600 on the next trade: equity $98,900, account breached — despite never having banked a meaningful gain and finishing only 1.1% below where you started. Under an end-of-day trailing rule, the same sequence survives, because the intraday peak never became the mark.

**The near-passing squeeze.** Trailing floors are tightest exactly when you are closest to your profit target: the more you have made, the higher the floor, and the less room each subsequent trade has. Traders who keep full size after a strong run are risking the account at its most fragile configuration.

**Rule variants matter.** Some firms trail only until the floor reaches the starting balance and then lock it (breakeven lock); some trail on end-of-day balance; some trail on real-time equity; withdrawals can reset or lower the mark. These distinctions change correct play significantly, and they differ enough across providers that reading the specific contract is non-negotiable — our [prop firms hub](/prop-firms/) breaks down the common structures.

## Managing drawdown proactively

Drawdown management that starts after the drawdown is damage control; the effective version is pre-committed.

1. **Budget the drawdown before trading.** Decide how much of the firm's limit you are willing to use — a personal maximum at roughly half to two-thirds of the firm's line leaves room for slippage and error.
2. **Graduate your response.** A workable structure: at one-third of your personal budget used, cut position size by half; at two-thirds, stop and conduct a full review before the next trade. Cutting size in drawdown slows the approach to the floor and shrinks the recovery bill simultaneously.
3. **Never raise size to recover.** The recovery table above tempts traders to "earn back faster." Doing so increases the probability of deepening the drawdown at exactly the point where each additional percent costs the most — the drawdown version of the spiral covered in [handling losing streaks](/psychology/handling-losing-streaks/).
4. **Bank progress against trailing rules.** On equity-trailing accounts, taking partial profits converts floating gains into cushion you control, rather than a higher floor you must defend.

## Key takeaways

- Absolute drawdown measures from the starting balance with a fixed floor; trailing drawdown measures from the high-water mark with a floor that only rises.
- The same equity path can measure 2.5% under an absolute rule and 6.25% under a trailing rule — know which one governs your account before your first trade.
- Recovery is asymmetric by exact math: 10% down needs 11.1% back, 20% needs 25%, 50% needs 100%.
- On equity-trailing funded accounts, unrealized profit raises your failure floor, so you can breach while above your starting balance.
- Pre-commit graduated responses — reduce size early in a drawdown, never increase it — because shallow drawdowns are cheap to repair and deep ones are structurally expensive.
