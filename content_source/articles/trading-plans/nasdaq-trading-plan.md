---
title: "NAS100 Trading Plan: A Structural Framework"
description: "A structural trading plan for NAS100/US100 — session timing, wider point-based stops, smaller size, and example funded-account risk parameters."
hub: "trading-plans"
updated: "2026-07-07"
reading_time: 8
order: 3
faq:
  - q: "Why do NAS100 stops need to be so much wider than forex stops?"
    a: "Because the instrument's normal noise is measured in tens of points, not fractions of one. NAS100 routinely covers several hundred points in a day, and ordinary intraday fluctuations can span 30 to 80 points without any change in structure. A stop sized like a forex stop sits inside that noise and gets hit by random movement rather than by the trade idea being wrong."
  - q: "What position size is appropriate for NAS100 on a funded account?"
    a: "Size is always derived, never chosen directly: divide your risk amount by the stop distance in points, then by the point value of your contract. A trader risking 0.5% of a 100,000 account with a 60-point stop risks 500 dollars across 60 points, which dictates a small position. Run your own numbers through a calculator rather than copying someone else's lot size."
  - q: "When is NAS100 most active during the day?"
    a: "Activity concentrates around the US cash equity open at 9:30 a.m. New York time, when volume and range expansion are typically at their highest, and around major US economic releases such as CPI and FOMC decisions. Many intraday plans focus exclusively on the first one to two hours after the open and stand aside during scheduled release windows."
  - q: "Can I trade NAS100 with the same plan I use for EUR/USD?"
    a: "The plan structure transfers — sessions, setups, risk limits, review — but every parameter must be recalibrated. Stop distances, position size, expected range, and news sensitivity are all different by an order of magnitude or more. Treating the two interchangeably is one of the most common causes of funded-account breaches on index instruments."
related:
  - { title: "NAS100 Position Size Calculator", href: "/calculator/nas100/" }
  - { title: "How to Build a Trading Plan", href: "/trading-plans/how-to-build-a-trading-plan/" }
  - { title: "Daily Loss Limits", href: "/risk-management/daily-loss-limits/" }
---

NAS100 punishes borrowed habits. Traders arrive from forex with stop distances, position sizes, and expectations calibrated to EUR/USD — and the index dismantles all three in a week. The instrument is not harder to trade; it is differently scaled, and a plan that does not respect the scale fails regardless of how good the setups are.

This is a structural framework for building a NAS100 plan: what the instrument's characteristics force you to decide, and example parameters for a funded account. It follows the general architecture in [how to build a trading plan](/trading-plans/how-to-build-a-trading-plan/) — this article covers only what NAS100 changes.

## What You're Actually Trading

NAS100 (also listed as US100 or USTEC, depending on the broker) tracks the Nasdaq-100 index of large-cap US stocks, dominated by technology names. Three characteristics drive every plan decision:

**Point value.** On most CFD offerings, one standard lot pays or costs the account currency equivalent of one unit per point of index movement, with the exact value depending on your broker's contract specification. Check yours before writing a single risk number — the specification, not habit, defines your exposure.

**Range.** NAS100's daily range is often several hundred points. Intraday swings of 50–100 points can occur inside a single hour without any news catalyst. This is the number that makes forex-calibrated stops unusable: a 10-point stop on NAS100 is the statistical equivalent of a stop measured in fractions of a pip.

**Volatility clustering.** Movement is not evenly distributed across the day. It concentrates around the US cash open (9:30 a.m. New York) and around US economic releases — CPI, FOMC, employment data. Quiet periods between those windows can be genuinely quiet, which matters for both opportunity and boredom-driven mistakes.

## Session Structure: Build Around the US Open

Because activity clusters at the cash open, most intraday NAS100 plans define their trading window around it. A common professional structure:

- **Preparation** before 9:30 NY: mark the overnight range, prior day's high/low, and any scheduled releases (see the [daily trading routine](/trading-plans/daily-trading-routine/) for the full pre-session checklist)
- **Primary window**: 9:30–11:30 NY, when range expansion and follow-through are typically strongest
- **Stand aside**: scheduled release windows, per a written rule — flat two minutes before, no entry until a defined period after
- **Afternoon**: many plans simply exclude it; liquidity thins and ranges compress until the final hour

A narrow window is not a limitation. It is the plan doing its job: concentrating your exposure where your tested edge lives.

## Why Stops Are Wider and Size Is Smaller

The core equation never changes: **position size = risk amount ÷ (stop distance × point value)**. On NAS100, the stop distance term is large, so the size term must be small. That is the whole adjustment, and refusing it is the root of most index-account failures.

A structurally placed NAS100 stop — beyond the opening range, beyond a swing point, or scaled to current volatility — commonly lands 40 to 100+ points from entry. Accept that distance and let size absorb it. The failure pattern runs the other way: a trader keeps the size they are used to, tightens the stop to keep the currency risk familiar, and then watches ordinary noise stop them out of directionally correct trades. Tight stop plus full size is not conservative on NAS100; it is a random-outcome generator.

Run the actual numbers in the [NAS100 calculator](/calculator/nas100/) rather than estimating — the sizing math itself is covered there and in the [position sizing guide](/risk-management/position-sizing/), so your plan only needs to record the resulting rules.

## Example Funded-Account Risk Parameters

The table below shows one internally consistent parameter set for a 100,000-unit funded account with a 5% daily loss limit imposed by the firm. It is a template to adapt, not a recommendation to copy.

| Parameter | Example value | Rationale |
| --- | --- | --- |
| Risk per trade | 0.5% (500 on a 100k account) | Small enough that a normal losing streak stays far from firm limits |
| Stop placement | Structure-based, typically 40–100 points | Outside ordinary intraday noise; never widened after entry |
| Position size | Derived per trade: 500 ÷ stop points ÷ point value | Size floats with stop distance; risk stays constant |
| Max trades per day | 3 | Caps exposure to the open window; prevents revenge sequences |
| Personal daily stop | −1.5% | Leaves a wide buffer inside the firm's 5% limit — see [daily loss limits](/risk-management/daily-loss-limits/) |
| News rule | Flat through major US releases | Spreads widen and slippage risk spikes at release time |
| Management | Partial at +1R, stop to entry, remainder to structure | Pre-decided; no live improvisation |

Note what the table does not contain: a fixed lot size. On NAS100, a fixed size with variable stops means variable risk — the opposite of what a funded account needs.

## Common Mistakes on NAS100

- **Sizing it like EUR/USD.** The signature error. Same lots, same stop distance in "points," catastrophically different currency risk. Every parameter must be derived from NAS100's own scale.
- **Trading the quiet hours out of boredom.** The edge that exists at 9:45 NY often does not exist at 13:30. Trades outside the window are untested by definition.
- **Tightening stops to afford bigger size.** Inverts the sizing equation and converts a strategy into noise-harvesting.
- **Holding through scheduled releases.** A position through CPI is not a trade; it is an unpriced event bet, and funded-account limits are unforgiving of the bad outcomes.
- **Averaging into losers.** With ranges this large, "it can't go further" is a sentence the index disproves several times a month.

## Key Takeaways

- NAS100's daily range — often several hundred points — is the single fact from which every plan parameter must be derived.
- Build the trading window around the US cash open, where volume and range expansion concentrate; exclude scheduled release windows in writing.
- Stops must be structurally placed and wide by forex standards; position size, not stop distance, is the variable that absorbs risk.
- On a funded account, set risk per trade (e.g., 0.5%) and a personal daily stop well inside the firm's limits, and derive size fresh for every trade.
- The most expensive mistake is transplanting forex sizing habits; use the NAS100 calculator and let the instrument's own numbers set your parameters.
