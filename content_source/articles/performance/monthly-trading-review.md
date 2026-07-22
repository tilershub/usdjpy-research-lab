---
title: "The monthly trading review: a structured process for funded traders"
description: "A structured monthly review: aggregate stats, plan-adherence rate, best and worst trades, rule violations, and one process change at a time."
hub: "performance"
updated: "2026-07-07"
reading_time: 8
order: 4
faq:
  - q: "Why review monthly instead of weekly or after every trade?"
    a: "Each cadence has a different job. Post-trade notes capture facts while they are fresh, and weekly reviews keep the journal current and spot acute problems. But structural conclusions need sample size: a month typically accumulates enough trades for statistics like win rate and expectancy to mean something, while a single week is mostly noise. The monthly review is where evidence becomes decisions; the shorter cadences just gather the evidence."
  - q: "Why only one process change per month?"
    a: "Because changes are experiments, and experiments need controlled conditions. If you alter your stop placement, your session times, and your setup filter simultaneously, next month's results cannot tell you which change helped or hurt. One change per month keeps cause and effect legible. It also protects against the churn failure mode, where a trader redesigns the system every few weeks and never accumulates a clean sample of anything."
  - q: "What should I do if my plan-adherence rate is low but the month was profitable?"
    a: "Treat it as a warning, not a success. A profitable month with poor adherence means variance paid you for behavior that will eventually charge you — undisciplined trading shows its true cost on the market's schedule, not yours. The review response is the same as for an unprofitable, low-adherence month: identify the most frequent violation, trace its trigger, and make fixing it the single process change for the coming month."
  - q: "How is a monthly review different for a funded trader than a personal-account trader?"
    a: "The stakes and the constraints differ. A personal account can survive a bad month and rebuild; a funded account has drawdown and daily-loss rules that can end it permanently, and a withdrawal schedule that rewards consistency. For funded traders the review therefore weighs rule violations and maximum drawdown more heavily than raw return, because the account's survival — not the month's P&L — is the asset being managed."
related:
  - { title: "The professional trading journal", href: "/performance/trading-journal-guide/" }
  - { title: "Expectancy explained", href: "/performance/expectancy-explained/" }
  - { title: "Managing a funded account", href: "/prop-firms/managing-a-funded-account/" }
---

A funded account is not lost in a month; it is lost in an afternoon — but the conditions for that afternoon are usually built over weeks of unexamined drift. Size creeps up. A setup gets looser. A rule gets bent once without consequence, then becomes negotiable. The monthly review is the mechanism that catches drift while it is still cheap to correct, and for a funded trader it is less a performance ritual than an account-survival practice. It takes one to two hours, runs on data your [trading journal](/performance/trading-journal-guide/) already holds, and follows the same structure every month.

## Step 1: aggregate the statistics

Compute the month's core numbers before forming any opinion about the month. Opinions formed first have a way of selecting their evidence.

- **Trades taken** — also your sample-size context for everything below
- **Win rate** and **average win / average loss in R**
- **Expectancy per trade** — the formula and its sample-size caveats are covered in [expectancy explained](/performance/expectancy-explained/)
- **Profit factor** — gross profit ÷ gross loss; see [win rate and profit factor](/performance/win-rate-and-profit-factor/) for how to read it alongside win rate
- **Total R for the month** and **maximum drawdown**, in R and as a percentage of the account
- **Distance from firm limits** — how close the worst day came to the daily loss limit, and the low-water mark against maximum drawdown

For a funded trader the last line is the headline. A month that gained 6R but touched 90% of the maximum drawdown was a near-death experience wearing a good month's clothes. The drawdown rules themselves live in the [risk management hub](/risk-management/); the review's job is to measure your actual distance from them.

## Step 2: measure plan adherence — separately from P&L

Compute the percentage of trades graded A or B for plan adherence, and put it next to the month's profitability. The two-by-two that results is the single most useful diagnostic in the review:

- **Profitable, high adherence** — the system works and you executed it. Change as little as possible.
- **Unprofitable, high adherence** — you executed correctly and the strategy underperformed. This is either normal variance or a genuine edge problem; the sample size decides which, and the response is patience or strategy review — not behavioral panic.
- **Profitable, low adherence** — the most dangerous quadrant. Variance rewarded indiscipline this month; it will not keep doing so. Treat this as a red flag with a bonus attached.
- **Unprofitable, low adherence** — you do not yet know whether the strategy works, because it was not the strategy that traded. Fix execution before judging the edge.

This separation is the entire reason adherence is graded per trade in the journal, and it is the difference between reviewing your trading and merely reviewing your luck. The behavioral machinery for improving a low adherence score is covered in [trading discipline](/psychology/trading-discipline/).

## Step 3: best and worst trade analysis

Pull the single best and worst trades of the month — by R, not by feeling — and interrogate each the same way: Was it within plan? What was the setup grade at entry? Was size correct per the [position sizing rules](/risk-management/position-sizing/)? What was the emotional-state note?

The worst trade usually teaches more. If it was a within-plan, correctly sized loss, it is simply the cost of doing business and requires no action. If it was oversized, unplanned, or a stop that got moved, it is a specimen of exactly the behavior that ends funded accounts — and its trigger (time of day, preceding loss, particular instrument) is next month's watch item. The best trade deserves equal skepticism: a big winner that violated the plan is not a template, it is a payout that will teach you the wrong lesson if you let it.

## Step 4: count rule violations

Count every violation of your written [trading plan](/trading-plans/how-to-build-a-trading-plan/) — oversized positions, trades outside session hours, skipped stops, exceeded daily trade counts — regardless of outcome. The count matters more than the consequences this month, because violations are drawdown that hasn't been charged yet. A month with zero violations and mediocre returns is a better month, for the longevity of a funded account, than a strong month with five. Sustained withdrawal eligibility, which is the actual product of a funded account, is built on exactly this consistency — the longer arc is covered in [managing a funded account](/prop-firms/managing-a-funded-account/).

## Step 5: choose one process change — at most

Everything above is diagnosis; this is the only prescriptive step, and it is deliberately constrained: **one process change per month, maximum.** One change keeps cause and effect readable in next month's data. It also breaks the churn cycle in which a trader redesigns the system every few weeks and never accumulates a clean sample of anything — a quiet but common way to stay permanently unproven.

The change should target the month's most expensive finding, be written as a rule ("no entries in the first 15 minutes of the session"), and be measurable in next month's review. If the month was profitable with high adherence, the correct number of changes is frequently zero.

## The review checklist

| # | Item | Output |
|---|---|---|
| 1 | Aggregate stats: trades, win rate, avg win/loss (R), expectancy, profit factor | One summary row per month |
| 2 | Max drawdown and worst day vs. firm limits | Distance-to-limit note |
| 3 | Plan-adherence rate (% of trades graded A/B) | Quadrant classification |
| 4 | Best trade autopsy (by R) | Within plan? Lesson or fluke? |
| 5 | Worst trade autopsy (by R) | Trigger identified, watch item set |
| 6 | Rule violations counted and categorized | Count + most frequent type |
| 7 | Last month's process change evaluated | Keep, revert, or extend |
| 8 | One process change selected (or none) | Written rule for next month |
| 9 | Next review scheduled | Fixed date on the calendar |

Item 7 closes the loop: last month's experiment gets a verdict before a new one begins. Keep each month's summary row in a single sheet — after six months, that table is the most honest performance record you own, and the foundation for everything else in the [performance hub](/performance/).

## Key takeaways

- Review monthly because a month is roughly the smallest sample where statistics like expectancy and profit factor start to mean something.
- Compute the numbers before forming opinions, and weigh distance-to-drawdown-limits as heavily as returns — for a funded account, survival is the product.
- Classify the month by profitability *and* plan adherence together; a profitable low-adherence month is a warning, not a win.
- Autopsy the best and worst trades by R, and count rule violations regardless of whether they cost money this time.
- Make at most one process change per month, written as a rule, and grade it at the next review before changing anything else.
