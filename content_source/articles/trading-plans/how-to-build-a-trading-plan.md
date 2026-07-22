---
title: "How to Build a Trading Plan: The Complete Framework"
description: "The six components of a complete trading plan — instruments, sessions, setups, risk parameters, management rules, and review — with a working template."
hub: "trading-plans"
updated: "2026-07-07"
reading_time: 9
order: 1
faq:
  - q: "How detailed does a trading plan need to be?"
    a: "Detailed enough that another competent trader could read it and execute your strategy without asking you a single question. If a rule requires interpretation in the moment — phrases like 'strong momentum' or 'good level' — it is not yet a rule. Every entry condition, risk figure, and exit action should be defined in objective, checkable terms before the session starts."
  - q: "Should my trading plan change for a funded account versus a personal account?"
    a: "The strategy usually stays the same, but the risk parameters must adapt to the account's constraints. Funded accounts carry daily loss limits and maximum drawdown rules that personal accounts do not. A funded-account plan typically sets risk per trade and a daily stop well inside the firm's limits, leaving a buffer so one bad session never threatens the account itself."
  - q: "How often should I revise my trading plan?"
    a: "Review performance weekly, but revise the plan itself on a fixed schedule — monthly or quarterly — and only with data. Changing rules mid-week after a losing streak is usually emotion, not analysis. A useful discipline is to write proposed changes in your journal, let them sit until the scheduled review, and only then decide with a sample of trades in front of you."
  - q: "What is the most common mistake traders make when writing a plan?"
    a: "Writing entry criteria in detail while leaving risk and exit rules vague. Most traders can describe their setup, but far fewer can state their exact risk per trade, daily loss limit, and the precise conditions under which they take partial profits or move a stop. Losses come from the unplanned parts of trading, so the risk section deserves the most precision, not the least."
related:
  - { title: "Daily Trading Routine", href: "/trading-plans/daily-trading-routine/" }
  - { title: "Position Sizing Guide", href: "/risk-management/position-sizing/" }
  - { title: "Trading Journal Guide", href: "/performance/trading-journal-guide/" }
---

A trading plan that lives in your head is not a plan. It is a set of intentions, and intentions degrade under pressure — usually at the exact moment you need them most. The working definition used across the [Trading Plans hub](/trading-plans/) is simple: **a plan is only a plan if it is written down and specific enough that another trader could execute it without asking you anything.** That standard sounds strict. It is also the difference between a strategy and a mood.

This guide walks through the six components every complete plan needs, in the order you should define them.

## 1. Market and Instrument Selection

Start by naming exactly what you trade — and, just as importantly, what you do not. "Indices and forex" is not a selection. "NAS100 and EUR/USD only" is.

Restricting your instrument list does three things. It concentrates your screen time so you learn one instrument's behavior deeply. It makes your journal data comparable, because 50 trades on one instrument tell you far more than 50 trades scattered across ten. And it removes the temptation to chase whatever happens to be moving on a given day.

Each instrument you trade needs its own parameter set — the stop distances and sizing that work on a forex pair do not transfer to an index. The [NAS100 plan](/trading-plans/nasdaq-trading-plan/) and [gold plan](/trading-plans/gold-trading-plan/) in this hub show how instrument-specific those numbers get.

## 2. Session and Time Windows

Define when you are allowed to trade, to the minute. Most intraday edges are session-dependent: a breakout strategy that performs around the US cash open may produce nothing but chop in the Asian session. Your plan should state:

- **Trading window** — e.g., 09:30–11:30 New York time, nothing outside it
- **No-trade periods** — the first two minutes after a major economic release, the last 15 minutes before you must leave the desk
- **Days off** — many traders exclude days with major scheduled events (FOMC, CPI, NFP) or reduce size on them

A time window is one of the cheapest risk controls available. Trades taken outside your window are, by definition, outside your tested edge.

## 3. Setup Definitions (Entry Criteria)

This is where most plans fail the "another trader could execute it" test. Write each setup as a checklist of objective conditions, all of which must be true before entry. Compare:

- Vague: "Enter on a pullback in a trend."
- Executable: "Price above the 20 EMA on the 5-minute chart; pullback touches the EMA zone; entry on the close of the first 5-minute candle that closes back above the pullback high; no entry if the pullback exceeded 50% of the prior leg."

If two of your setups can fire at once, state which takes priority. If a condition is discretionary, either make it objective or delete it. A plan with one fully defined setup outperforms a plan with five loosely sketched ones, because only the defined setup produces journal data you can actually evaluate — the foundation of the review process covered in the [trading journal guide](/performance/trading-journal-guide/).

## 4. Risk Parameters

Risk parameters are the section that keeps you funded. Three numbers are non-negotiable:

- **Risk per trade** — a fixed percentage of account equity, commonly 0.25%–1%. On funded accounts, the lower end is standard practice.
- **Daily loss limit** — the point at which you stop trading for the day, set inside any limit your prop firm imposes. See [daily loss limits](/risk-management/daily-loss-limits/) for how to set the buffer.
- **Maximum trades per day** — a cap (often 2–4) that prevents overtrading and revenge sequences.

Risk per trade defines position size, not the other way around: size = risk amount ÷ stop distance. Use the [position size calculator](/tools/position-size-calculator/) to run the math per instrument rather than estimating. The full logic lives in the [Risk Management hub](/risk-management/).

## 5. Trade Management Rules

Decide before entry what happens after entry. Your plan should answer, in writing:

- **Initial stop** — where it goes and why (structure-based, ATR-based, or fixed), and the rule that it never widens
- **Target** — fixed R multiple, structural level, or trailing method
- **Partials** — whether you scale out, at what level, and what happens to the stop afterward
- **Time stop** — what you do if the trade goes nowhere for a defined period

Ambiguity here is where discipline leaks. A trader who has not pre-decided their partial-exit rule will decide it live, under P&L pressure — and live decisions correlate poorly with good ones, as the work on [trading discipline](/psychology/trading-discipline/) covers in depth.

## 6. Review Process

A plan without a review loop cannot improve. Specify the cadence: journal every trade the same day, review the week every Friday or Sunday, and evaluate the plan itself monthly or quarterly. Critically, **rule changes happen only at scheduled reviews, with data** — never mid-session, never after a single losing day.

## Trading Plan Template

| Plan section | What it must specify | Example entry |
| --- | --- | --- |
| Instruments | Exact symbols traded, nothing else | NAS100, XAU/USD only |
| Session window | Days and times, with timezone | Mon–Thu, 09:30–11:30 NY; no trades on FOMC days |
| Setup(s) | Objective checklist per setup | 5-min opening range breakout; all 4 checklist conditions required |
| Risk per trade | Fixed % of equity | 0.5% of current equity |
| Daily loss limit | Hard stop for the day | −1.5% or 2 consecutive losses, whichever first |
| Max trades/day | Numerical cap | 3 |
| Stop rule | Placement method; never widened | Beyond range extreme + volatility buffer |
| Target / partials | Exit structure | 50% off at +1R, stop to entry, runner to +2R |
| Review cadence | Journal + review schedule | Journal daily; weekly review Sunday; plan revision monthly |

Copy this table, replace every example with your own entry, and check each row against the test: could someone else execute it? Any row that fails is where your next losing streak is hiding.

## Key Takeaways

- A plan must be written and specific enough for another trader to execute without questions — anything less is intention, not a plan.
- Six components make a plan complete: instruments, time windows, setup definitions, risk parameters, management rules, and a review process.
- The risk section (risk per trade, daily limit, max trades) deserves the most precision, especially on funded accounts with firm-imposed limits.
- Trade management decisions — stops, targets, partials — are made before entry, in writing, never live under P&L pressure.
- Rules change only at scheduled reviews, backed by journal data, never mid-session after a losing trade.
