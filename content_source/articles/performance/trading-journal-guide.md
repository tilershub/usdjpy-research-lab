---
title: "The professional trading journal: what to capture and why"
description: "What a professional trading journal records before, during, and after each trade — and why plan adherence matters more than P&L."
hub: "performance"
updated: "2026-07-07"
reading_time: 8
order: 1
faq:
  - q: "What should a trading journal include beyond entry and exit prices?"
    a: "A professional journal captures three layers: the pre-trade plan (setup type, intended entry, stop, target, and risk), the execution record (actual fills, size, and a chart screenshot), and the post-trade review (outcome in R-multiples, a plan-adherence grade, and a note on emotional state). The platform already stores your prices. The journal exists to store your decisions, which no platform records for you."
  - q: "Why should I grade plan adherence separately from profit and loss?"
    a: "Because over a small number of trades, P&L is dominated by variance while adherence is fully within your control. A trade that followed every rule and lost is evidence your process ran correctly; a trade that broke rules and won is a warning disguised as a reward. Grading adherence separately lets you evaluate the decision quality directly instead of letting short-term outcomes mislead you."
  - q: "Is a spreadsheet good enough, or do I need journaling software?"
    a: "A spreadsheet is entirely sufficient and is often the better starting point. It is free, fully customizable, and forces you to define your own fields, which is itself a useful exercise. Dedicated apps add automatic trade imports, chart capture, and built-in analytics, which matter more as trade frequency rises. Start with a spreadsheet; switch only when manual entry becomes the reason you skip journaling."
  - q: "How long should each journal entry take?"
    a: "For most traders, two to three minutes per trade is realistic once the template is fixed: the pre-trade fields are filled before entry, and the review fields take a minute after the close. The weekly aggregation takes twenty to thirty minutes. If entries routinely take longer, the template is too elaborate — cut fields until the habit is sustainable, because a simple journal you keep beats a thorough one you abandon."
related:
  - { title: "Expectancy explained", href: "/performance/expectancy-explained/" }
  - { title: "The monthly trading review", href: "/performance/monthly-trading-review/" }
  - { title: "How to build a trading plan", href: "/trading-plans/how-to-build-a-trading-plan/" }
---

Your broker already records every price, timestamp, and fill. If a journal only repeats that data, it adds nothing. What no platform records — and what separates traders who improve from traders who repeat themselves — is everything around the trade: what you planned to do, whether you did it, and what state you were in at the time. A professional trading journal is a record of decisions, not prices. Done properly, it becomes the raw data for every other [performance metric](/performance/) you will ever calculate.

## The three layers of a complete journal entry

A useful entry is written in three passes, at three different moments.

**Pre-trade (before entry).** Before risk goes on, you record the setup name, the planned entry, stop, and target, and the risk in both currency and account percentage. Writing this down before the fill is the point: it creates a commitment that the post-trade review can be graded against. If you cannot name the setup from your [trading plan](/trading-plans/how-to-build-a-trading-plan/), that is the journal telling you not to take the trade.

**Execution (during and at exit).** Actual entry and exit prices, position size, and a screenshot of the chart at entry. Screenshots matter more than they seem: six weeks later, "the setup looked clean" is unverifiable, but the chart is not. Size deserves its own field because size drift is the most common silent rule violation — the [position sizing guide](/risk-management/position-sizing/) covers how size should be determined, and the journal verifies that it was.

**Post-trade (after the close, once calm).** The outcome expressed in R-multiples — profit or loss divided by the amount initially risked — a plan-adherence grade, and a short note on emotional state. R-multiples normalize results across instruments and account sizes, which is what makes later analysis like [expectancy](/performance/expectancy-explained/) possible.

## The fields, and why each one earns its place

| Field | When recorded | Why it matters |
|---|---|---|
| Date / session | Pre-trade | Surfaces time-of-day and session patterns in aggregation |
| Setup name | Pre-trade | Ties the trade to a defined edge; enables per-setup stats |
| Planned entry / stop / target | Pre-trade | The commitment the trade is graded against |
| Risk (currency and % of account) | Pre-trade | Detects size drift before it compounds |
| Actual entry / exit / size | Execution | The factual record; deviations from plan become visible |
| Screenshot at entry | Execution | Verifiable evidence of what the setup actually looked like |
| Result in R | Post-trade | Normalized outcome; the input to expectancy and profit factor |
| Plan-adherence grade (A–D) | Post-trade | Measures the variable you control |
| Emotional state note | Post-trade | Links behavioral states to execution errors over time |
| One-line lesson | Post-trade | Forces a conclusion; prevents passive logging |

Every field either feeds a statistic or documents a decision. Anything that does neither — long narrative paragraphs, macro commentary, indicator readings you did not act on — is weight that makes the habit harder to keep.

## Grade the process, not the outcome

The single most important discipline in journaling is scoring plan adherence separately from P&L. A simple A–D scale works: A means every element of the plan was followed; D means the trade was improvised. The grade is assigned regardless of result.

This matters because the two scores frequently disagree. A losing trade that followed the plan exactly is a good trade — you paid the normal, expected cost of running a strategy with a losing percentage. A winning trade that broke the plan is a bad trade that happened to be paid for, and it trains exactly the behavior that ends funded accounts. Over a month, the adherence column tells you whether you have an execution problem or a strategy problem — two conditions with completely different fixes. Traders who skip this distinction usually end up "fixing" a strategy that was never broken, a pattern that shows up repeatedly in [why discipline is structural, not emotional](/psychology/trading-discipline/).

The emotional-state field serves the same purpose from another angle. One-word entries are enough: calm, rushed, frustrated, overconfident. In aggregation, these words correlate with adherence grades with uncomfortable reliability, and they are especially diagnostic during drawdowns — see the [losing streaks article](/psychology/handling-losing-streaks/) for how that data gets used.

## The weekly aggregation

Individual entries are data; the weekly pass is where they become information. Once a week, at a fixed time outside market hours, compute a small set of aggregates: number of trades, win rate, average win and loss in R, total R for the week, and — most importantly — the percentage of trades graded A or B for adherence. Then read the D-grade trades and look for the shared trigger: a time of day, a preceding loss, a particular instrument.

The weekly review deliberately stays descriptive. You are looking for one observation, not redesigning the system; structural changes belong in the [monthly review](/performance/monthly-trading-review/), where the sample is large enough to justify them.

## Spreadsheet or app

| | Spreadsheet | Dedicated journaling app |
|---|---|---|
| Cost | Free | Typically subscription |
| Customization | Total — your fields, your grades | Limited to the vendor's model |
| Data entry | Manual (friction, but forces reflection) | Automatic broker import |
| Screenshots | Linked or pasted manually | Usually captured in-app |
| Analytics | You build them (and understand them) | Built-in dashboards |
| Failure mode | Entry fatigue at high frequency | Passive logging without reflection |

The honest tradeoff: spreadsheets create friction that doubles as reflection; apps remove friction and, with it, sometimes the thinking. A reasonable path is to start in a spreadsheet until your fields and grades are stable, then move to an app only if manual entry is genuinely the bottleneck. Whichever you choose, the pre-trade fields must be filled before entry — a journal reconstructed at the end of the day is a diary, not an instrument.

## Key takeaways

- A journal records decisions, not prices — the pre-trade plan, execution against it, and a post-trade review are three separate passes.
- Express every outcome in R-multiples so results are comparable across instruments and feed directly into expectancy and profit factor.
- Grade plan adherence separately from P&L: a rule-following loss is a good trade, and a rule-breaking win is a warning.
- Aggregate weekly, but save structural changes for the monthly review when the sample supports them.
- Choose the tool you will actually use daily; a simple spreadsheet kept faithfully outperforms sophisticated software used sporadically.
