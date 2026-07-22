---
title: "Daily Loss Limits: Your Circuit Breaker Inside the Firm's"
description: "How prop firm daily loss limits work, why your personal limit should sit at 1-2%, and the exact math of how quickly losing trades reach a breach."
hub: "risk-management"
updated: "2026-07-07"
reading_time: 8
order: 3
faq:
  - q: "How do prop firm daily loss limits actually work?"
    a: "Most firms take a snapshot of your balance or equity at the start of the trading day, typically at a fixed server-time rollover, and set a hard floor 4-5% below it. If equity touches that floor at any point during the day, including on open floating losses at many firms, the account is breached. The limit resets at the next rollover, so a bad day never carries the deficit forward, but a single breach usually ends the account."
  - q: "Why should my personal daily limit be smaller than the firm's?"
    a: "The firm's limit is a termination line, not a target. If you routinely trade near it, one gap, one slippage event, or one impulsive trade ends the account. A personal limit of 1-2% keeps you far from the cliff edge, caps the damage any single impaired session can do, and preserves enough drawdown budget that a losing day is a data point rather than an emergency."
  - q: "How many losing trades does it take to breach a 5% daily limit?"
    a: "Divide the limit by your risk per trade. At 1% risk, the fifth consecutive loss lands exactly on a 5% limit, and slippage or commissions can push you through even earlier. At 2% risk, the third loss breaches. At 0.5% risk you would need ten straight losses in one session, which is why smaller per-trade risk makes the firm's daily limit almost impossible to hit accidentally."
  - q: "What should I do after hitting my personal daily limit?"
    a: "Stop trading immediately: close positions, cancel working orders, and shut the platform. Log what happened while it is fresh, but postpone judgments about your strategy until the next day. Before the next session, review the losses for rule violations versus normal variance, and only resume at standard size if the losses were within plan. Never begin the next day trying to win back the previous day's deficit."
related:
  - { title: "Risk of Ruin", href: "/risk-management/risk-of-ruin/" }
  - { title: "Drawdown Explained", href: "/risk-management/drawdown-explained/" }
  - { title: "Prop Firm Rules Explained", href: "/prop-firms/prop-firm-rules-explained/" }
---

Most funded accounts do not die from bad strategies. They die in single sessions — a cluster of losses, an attempt to trade back to flat, and a breach of a daily limit that existed precisely to prevent that sequence. The daily loss limit is the sharpest rule in prop trading because it operates on the shortest clock: you can respect your per-trade risk perfectly for months and still lose the account in one afternoon. Understanding how the firm's limit is calculated, and running a personal limit well inside it, is the difference between a system that survives bad days and one that merely hopes to avoid them.

## How prop firm daily limits are calculated

The standard mechanism is a snapshot-and-floor system. At a fixed daily rollover (commonly 5:00 PM ET or midnight server time), the firm records your balance — or the higher of balance and equity, depending on the firm — and sets a hard floor 4-5% below that snapshot. A $100,000 account with a 5% daily limit that starts the day at $102,000 has a floor of $96,900 for that session.

Three details routinely catch traders out:

- **Floating losses usually count.** At most firms, if open-position drawdown drags equity to the floor intraday, the account is breached even if the trade would have recovered.
- **The floor is fixed in dollars for the day.** It is set from the start-of-day snapshot, not recalculated as you lose. Winning earlier in the day, however, does not raise it either — profits give you cushion above the floor, not a lower floor.
- **A breach is terminal.** Unlike your own rules, the firm's limit has no next-day reset for the account itself — only for the limit. Firm-by-firm variations are covered in our [prop firm rules guide](/prop-firms/prop-firm-rules-explained/).

## The math of a breach

Because the firm's floor is a fixed dollar amount below the start-of-day balance, and because most traders size positions from that same balance, the arithmetic of a breach is simple division: the number of consecutive full losses that reach the limit is the limit divided by risk per trade. The table shows how quickly a bad session escalates at different risk levels, alongside a 1.5% personal limit for comparison.

| Risk per trade | Losses to breach 4% firm limit | Losses to breach 5% firm limit | Losses to hit a 1.5% personal limit |
|---|---|---|---|
| 0.25% | 16 | 20 | 6 |
| 0.5% | 8 | 10 | 3 |
| 1% | 4 | 5 | 2 |
| 2% | 2 | 3 | 1 |
| 3% | 2 | 2 | 1 |

Two things stand out. First, at 2-3% risk per trade, the firm's limit is two or three trades away at all times — a normal cold streak, not a catastrophe, is enough to end the account in a single session. Second, the numbers above assume clean, full-size stop-outs. Slippage through a stop, commissions, and any position that was oversized because of a miscalculated pip value all push the real breach point earlier. Sizing each position precisely — use the [position size calculator](/tools/position-size-calculator/) rather than mental arithmetic — is part of daily-limit discipline, not separate from it.

## Why your personal limit belongs at 1-2%

The firm's 5% is a legal boundary, not an operating guideline, and treating it as available budget is a category error for three reasons.

**Buffer against the terminal event.** A personal limit at 1.5% means that even a maximally bad day leaves 3.5% of headroom before anything irreversible happens. Gaps, news spikes, and platform issues land on cushion instead of on the breach line.

**Decision quality degrades before the limit does.** The research on loss-day psychology aside, the structural point is mathematical: every trade taken while "down on the day" carries the temptation of increased size, and increased size is exactly what accelerates the table above. A tight personal limit removes you from the session before the degraded decisions get made — the failure pattern dissected in our article on [revenge trading](/psychology/revenge-trading/).

**Daily limits protect the monthly drawdown.** A 1.5% worst day means even four maximum-loss days in a week cost about 6% — painful but recoverable. Two 5% days in the same week put most funded accounts at or beyond their overall drawdown limit. The daily limit is the mechanism that keeps any single day from consuming the survival budget analyzed in [risk of ruin](/risk-management/risk-of-ruin/).

A sensible structure: personal daily limit of 1-2% of start-of-day balance, sized so it equals two to three full losses at your standard per-trade risk. A trader risking 0.5% per trade with a 1.5% daily stop gets exactly three attempts per session — enough to trade a plan, too few to spiral.

## Implementation: rules that fire without you

A daily limit that depends on in-the-moment willpower is a suggestion, not a limit. Implementation has three layers:

1. **Hard rules, written down.** Define the limit as a dollar figure each morning (e.g., "start-of-day $101,400, daily stop at $99,880"), not a percentage you compute while tilted. Define what counts: realized plus floating, measured at the worst point, matching how your firm measures it.
2. **Platform enforcement.** Use whatever automation your stack allows — daily loss settings in the trade copier or risk manager, platform-level equity guards, or at minimum a rule that hitting the number means flatten everything, cancel all orders, and close the platform for the day. Physically ending the session is the enforcement mechanism; staying "just to watch" reliably becomes staying to trade.
3. **Next-day protocol.** The evening of a limit day, log the trades and classify each loss: within plan, or rule violation. If losses were within plan, resume the next day at standard size — variance is the cost of doing business, as covered in [handling losing streaks](/psychology/handling-losing-streaks/). If rules were broken, the next day starts at reduced size or in review-only mode. In neither case does the next day's plan include "recovering" yesterday; the deficit is sunk, and the only job is executing the process.

## Key takeaways

- Prop firm daily limits are hard floors set 4-5% below a start-of-day snapshot; floating losses typically count, and one breach ends the account.
- The breach math is division: at 1% risk per trade, five consecutive losses reach a 5% limit; at 2% risk, three losses do — before slippage and commissions.
- A personal limit of 1-2% keeps a full bad day well inside the firm's line and stops the session before decision quality collapses.
- Set your daily limit at two to three full losses at standard risk: enough attempts to trade the plan, too few to spiral.
- Enforcement must be mechanical — a preset dollar number, platform-level guards, and a written next-day protocol — because a limit enforced by willpower fails exactly when it is needed.
