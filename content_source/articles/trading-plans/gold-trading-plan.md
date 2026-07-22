---
title: "Gold (XAU/USD) Trading Plan: A Structural Framework"
description: "A structural trading plan for XAU/USD — point value mechanics, session behavior, news sensitivity, and example funded-account risk parameters."
hub: "trading-plans"
updated: "2026-07-07"
reading_time: 8
order: 4
faq:
  - q: "Why is gold considered harder to size than forex pairs?"
    a: "Because its point value and typical range combine unforgivingly. On a standard lot, each 0.1 move in the quoted price — one point — is worth about 10 dollars, and gold can travel hundreds of points in a session. A lot size that feels routine on a forex pair can therefore expose several times the intended risk on XAU/USD, which is why size must always be derived from the stop distance."
  - q: "When is XAU/USD most active during the trading day?"
    a: "Activity typically builds through the London session and peaks during the London–New York overlap, when both major trading centers are open. US economic releases and Federal Reserve communications add sharp bursts of movement on top of that baseline. Many gold plans concentrate their trading window on the overlap and stand aside during scheduled release windows."
  - q: "How should a funded trader handle gold around Fed and CPI releases?"
    a: "With a written rule decided before the day begins. Gold reacts strongly to interest-rate expectations, so releases like CPI, FOMC decisions, and press conferences can produce fast, gapping moves with widened spreads. Common professional choices are to be flat through the release window, to halve risk for the entire day, or to skip the day. Improvising at release time is not a plan."
  - q: "Is the same risk percentage appropriate for gold as for other instruments?"
    a: "The percentage can be the same — many funded traders use 0.5% per trade across instruments — but the resulting position size will differ substantially. Because gold's stops are wide in points and each point is expensive per lot, the same 0.5% typically produces a much smaller lot size on XAU/USD than on a major forex pair. Constant risk, variable size."
related:
  - { title: "XAU/USD Position Size Calculator", href: "/calculator/xauusd/" }
  - { title: "NAS100 Trading Plan", href: "/trading-plans/nasdaq-trading-plan/" }
  - { title: "Position Sizing Guide", href: "/risk-management/position-sizing/" }
---

Gold has ended more funded accounts than most instruments, and rarely because the trader's analysis was wrong. The account-enders are structural: a lot size copied from forex, a stop placed inside gold's ordinary noise, a position held through a Fed press conference. XAU/USD rewards traders who respect its mechanics and removes those who do not — usually quickly.

This framework covers what a gold-specific plan must define. The general plan architecture — setups, windows, review — is covered in [how to build a trading plan](/trading-plans/how-to-build-a-trading-plan/); here we deal only with what gold changes.

## The Point Value Structure

Start with the arithmetic, because everything else follows from it. XAU/USD is quoted in US dollars per ounce, to two decimal places. In the convention used by most brokers and calculators:

- **One point = 0.1** of the quoted price (e.g., a move from 2,350.00 to 2,350.10)
- **One standard lot = 100 ounces**, so one point is worth **about $10 per standard lot**
- A full $1.00 move in the gold price is therefore 10 points — roughly **$100 per standard lot**

Now put that against gold's behavior: sessions that travel tens of dollars are unremarkable, which means hundreds of points against a position measured at $10 per point per lot. A single standard lot through a $15 adverse move is $1,500 — on many funded accounts, most or all of a day's loss allowance in one trade. This is the arithmetic behind the rule that gold demands smaller lots: the range is wide and every point is expensive, so size is the only variable left to control. The [position sizing guide](/risk-management/position-sizing/) covers the general method; the [XAU/USD calculator](/calculator/xauusd/) runs gold's specific numbers, so your plan records the rules rather than re-deriving the math.

## Session Behavior: Plan Around the Overlap

Gold trades nearly around the clock, but its liquidity and movement are not evenly distributed:

- **Asian session** — typically quieter, ranges often compressed; some plans exclude it entirely
- **London session** — activity builds; the European open frequently sets the day's first meaningful directional attempt
- **London–New York overlap** — usually the most active window of the day, with both major centers open and US data landing inside it
- **Late New York** — liquidity thins after London closes; spreads can widen into the daily close

A disciplined gold plan names its window explicitly — for many intraday traders, the overlap — and treats everything outside it as off-limits. The pre-session checks that make the window tradeable (news times, key levels, current range versus average) are the standard [daily trading routine](/trading-plans/daily-trading-routine/), applied to gold's clock.

## News Sensitivity: The Macro Instrument

Gold is a macro asset wearing a chart. It responds directly to US interest-rate expectations, which makes it acutely sensitive to:

- **Federal Reserve communications** — rate decisions, press conferences, minutes, and scheduled speeches
- **US inflation and employment data** — CPI above all, plus NFP and related releases
- **Geopolitical developments** — risk events can move gold sharply and without calendar warning

The scheduled items belong in your pre-session check with exact times and a written rule: flat through the window, reduced size for the day, or no trading that day. The unscheduled ones are why gold stops must always be real, resting orders — never mental. A mental stop during a geopolitical headline is a donation.

## Example Funded-Account Risk Parameters

One internally consistent parameter set for a 100,000-unit funded account with a firm-imposed 5% daily limit. Adapt the values to your own account and data; the structure is the point.

| Parameter | Example value | Rationale |
| --- | --- | --- |
| Risk per trade | 0.5% ($500 on a 100k account) | Keeps a normal losing streak far from firm thresholds |
| Stop placement | Structure-based, commonly 30–80 points ($3–$8) | Outside routine noise; hard stop in the market, never mental |
| Position size | Derived: $500 ÷ stop points ÷ $10 per point per lot | E.g., a 50-point stop → $500 ÷ 50 ÷ 10 = 1.0 lot equivalent; recalculated every trade |
| Max trades per day | 3 | Limits exposure and revenge sequences |
| Personal daily stop | −1.5% | Wide buffer inside the firm's 5% — see [daily loss limits](/risk-management/daily-loss-limits/) |
| News rule | Flat through Fed/CPI windows; half risk on release days | Spread widening and gaps make release-time risk unmeasurable |
| Management | Partial at +1R, stop to entry, remainder trailed on structure | Decided before entry, executed without negotiation |

The size row is the one to internalize: lot size is an output of the stop distance, recalculated per trade, never a fixed habit.

## Common Gold-Specific Errors

- **Forex-sized lots on gold moves.** The signature error, mirroring [the same mistake on NAS100](/trading-plans/nasdaq-trading-plan/): familiar size, unfamiliar point value, several times the intended risk.
- **Stops inside the noise.** A $1–$2 stop on an instrument that routinely oscillates several dollars intraday is a coin flip with commissions.
- **Holding through Fed events.** Gold's defining sensitivity. A position through a press conference is an event bet, not a setup.
- **Trading the dead hours.** Forcing entries in the quiet Asian session because the chart is open is boredom, not edge — a [discipline](/psychology/trading-discipline/) failure the trading window exists to prevent.
- **Mental stops.** Gold's headline-driven moves punish them disproportionately; only resting orders count.

## Key Takeaways

- Gold's mechanics are unforgiving: one point (0.1 of price) is worth about $10 per standard lot, and sessions covering hundreds of points are routine.
- Because the range is wide and each point is expensive, lot size must be derived from stop distance every trade — smaller than forex intuition suggests.
- Concentrate the trading window where gold is most active, typically the London–New York overlap, and exclude the dead hours in writing.
- Fed communications, CPI, and geopolitical headlines demand written news rules and real resting stops — never mental ones.
- On funded capital, 0.5% risk per trade with a personal daily stop well inside the firm's limit keeps an ordinary losing day survivable.
