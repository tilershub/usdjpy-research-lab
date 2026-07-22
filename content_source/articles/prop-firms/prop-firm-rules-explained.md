---
title: "Prop Firm Rules Explained: Every Rule That Can End Your Account"
description: "A complete guide to prop firm rules — daily loss limits, trailing drawdown, consistency rules, news restrictions, and what actually triggers a breach."
hub: "prop-firms"
updated: "2026-07-07"
reading_time: 9
order: 1
faq:
  - q: "What is the difference between a balance-based and equity-based daily loss limit?"
    a: "A balance-based limit is measured against your account balance at the start of the trading day, ignoring open positions. An equity-based limit includes floating profit and loss, so an open trade that moves against you can breach the limit even if you never close it at a loss. Equity-based limits are stricter and catch more traders off guard, so always confirm which model your firm uses."
  - q: "Why do most traders fail prop firm challenges?"
    a: "Industry commentary and firm statements consistently point to risk-rule violations, not missed profit targets, as the main failure mode. Traders breach the daily loss limit or maximum drawdown by sizing too large or adding to losers. The profit target rarely eliminates anyone directly — it is the attempt to reach it too quickly that triggers a loss-limit breach along the way."
  - q: "Can I hold trades over the weekend on a funded account?"
    a: "It depends entirely on the firm and often on the account type. Some firms allow weekend holding on swing-style accounts but prohibit it on standard accounts because of gap risk at the Sunday open. Holding through a prohibited weekend can void the account even if the trade wins, so verify the current rule for your specific account type before Friday's close."
  - q: "Are news-trading restrictions common at prop firms?"
    a: "Yes. Many firms restrict opening or closing positions within a window around high-impact releases — commonly a couple of minutes either side of events like nonfarm payrolls or central bank decisions. Some apply the restriction only on funded accounts, not during evaluation. The exact window, the affected instruments, and the penalty vary by firm, so check the current terms before every major release."
related:
  - { title: "How to Choose a Prop Firm", href: "/prop-firms/how-to-choose-a-prop-firm/" }
  - { title: "Daily Loss Limits", href: "/risk-management/daily-loss-limits/" }
  - { title: "Drawdown Explained", href: "/risk-management/drawdown-explained/" }
---

Most traders who fail a prop firm evaluation never miss the profit target. They breach a risk rule — usually the daily loss limit or the maximum drawdown — often within the first two weeks. The profit target gets all the attention in marketing material, but the rules that actually end accounts are the ones written in smaller print. Understanding every rule type before you pay for an evaluation is the single highest-return piece of preparation you can do.

This guide covers each major rule category used across the industry, what typically triggers a breach, and where traders most often get caught. Firms vary widely and change terms frequently, so treat everything here as a description of *typical* structures and verify current rules on your firm's official site. For how the challenge process itself works end to end, see the [Prop Firms hub](/prop-firms/).

## Profit Target

The profit target is the amount you must gain to pass an evaluation phase. In a typical two-step evaluation, Phase 1 targets are around 8–10% of the starting balance and Phase 2 targets around 4–5%. Once funded, most firms remove the target entirely — you simply trade and request payouts.

The target is rarely the problem. The problem is the behavior it induces: traders size up to hit it quickly, and oversized positions are what collide with the loss rules below.

## Daily Loss Limit: Balance-Based vs Equity-Based

The daily loss limit — typically around 5% of the account — is the rule that ends the most evaluations. The critical detail is *how it is measured*:

- **Balance-based:** the limit is calculated from your account **balance** at the start of the trading day (often 5pm ET or midnight CET). Only closed losses count against it. Floating drawdown on open trades does not breach the rule until realized.
- **Equity-based:** the limit is calculated against **equity**, which includes open positions. If your floating loss at any moment pushes equity below the day's threshold, the account is breached — even if the trade would have recovered.

Equity-based limits are the stricter and more common model. A trader holding an open position down 4.9% who lets it wick another 0.2% against them is finished, regardless of where the trade closes. Some firms also count the day's *realized profits* into the calculation, meaning a strong morning can raise the amount you are allowed to give back — while others anchor strictly to the start-of-day balance. This distinction is worth a careful read of the firm's FAQ. We cover how to build a personal buffer inside the firm's limit in [daily loss limits](/risk-management/daily-loss-limits/).

## Maximum Drawdown: Static vs Trailing

The maximum (overall) drawdown — typically around 10% — is the account's hard floor. Two models dominate:

- **Static drawdown:** the floor is fixed relative to the *initial* balance. A $100,000 account with a 10% static drawdown is breached at $90,000, full stop. Profits raise your cushion.
- **Trailing drawdown:** the floor *rises* as your equity or balance makes new highs. Early profits move the breach level up behind you, so a trader who runs the account to $105,000 may find the floor has trailed to $95,000 or higher. Some trailing models lock at the initial balance once you gain enough; others trail indefinitely.

Trailing drawdown is the most misunderstood rule in the industry and is especially common at futures-focused firms. The mechanics and math are covered in detail in [drawdown explained](/risk-management/drawdown-explained/).

## Minimum Trading Days

Most firms require a minimum number of trading days per phase — commonly around 3 to 10 — to prevent passing on one lucky oversized trade. A "trading day" usually means any day with at least one opened position. This rule rarely fails anyone, but it does stop traders from finishing a challenge in a single session.

## Consistency Rules

Consistency rules cap how much of your total profit can come from a single day or single trade — a common form limits any one day to a stated percentage (often somewhere around 30–50%) of total profit. The intent is to filter out gamblers. The trap: a trader who makes 80% of their profit on day one may need to *keep trading* additional profitable days to dilute that day's share before a payout or pass is granted. Some firms apply consistency rules only on funded accounts, some only during evaluation, some not at all.

## News-Trading Restrictions

Many firms restrict trading around high-impact scheduled news — typically prohibiting opening or closing positions within a short window (often around two minutes) either side of releases like nonfarm payrolls or rate decisions. Common variations: the restriction applies only on funded accounts, only to the directly affected instruments, or only to positions *opened* in the window. Penalties range from voided profits on the offending trade to full account breach.

## Weekend and Overnight Holding

Some firms require all positions closed before the weekend on standard accounts due to gap risk, while offering swing account types that permit holding. Crypto and futures rules differ again. Holding through a prohibited period can void the account even if the trade profits.

## Prohibited Strategies

Almost every firm prohibits a familiar list: high-frequency trading and tick scalping that exploits demo-server latency, latency or feed arbitrage, guaranteed-profit hedging across accounts or firms, and account management by third parties. Copy trading is a genuine gray area — copying *your own* trades across your own accounts at the same firm is often permitted, while copying another person's signals or trades usually is not. These rules are enforced most aggressively at payout time, which is exactly when you do not want a dispute.

## Payout Rules

Funded accounts typically pay a profit split in the region of 80% to the trader, on a cycle that ranges from weekly to monthly, sometimes with a minimum number of trading days between requests. Some firms impose a minimum payout amount or apply consistency checks before approving withdrawals. Read the payout terms *before* buying the evaluation — this is where reliability differences between firms show up most clearly, a topic we take further in [how to choose a prop firm](/prop-firms/how-to-choose-a-prop-firm/).

## Rule Types at a Glance

| Rule | Typical structure | What triggers a breach |
|---|---|---|
| Profit target | ~8–10% Phase 1, ~4–5% Phase 2 | Not a breach — just an unmet goal |
| Daily loss limit | ~5% of balance or equity | Closed losses (balance-based) or floating + closed losses (equity-based) crossing the daily threshold |
| Maximum drawdown | ~10%, static or trailing | Equity/balance falling below the fixed or trailing floor |
| Minimum trading days | ~3–10 days per phase | Not a breach — delays passing |
| Consistency rule | Single day capped at a % of total profit | Usually delays pass/payout rather than voiding the account |
| News restrictions | No trades ± a short window around high-impact events | Opening/closing in the window; may void profits or the account |
| Weekend holding | Prohibited on standard accounts at some firms | Any open position past the cutoff |
| Prohibited strategies | No HFT, latency arbitrage, cross-account hedging; copy-trade limits | Detected use — often enforced at payout review |
| Payout rules | ~80% split, weekly to monthly cycles | Not a breach — but violations elsewhere surface here |

## Key Takeaways

- The daily loss limit and maximum drawdown end far more accounts than the profit target ever does — build your risk plan around them first.
- Confirm whether your firm's daily limit is balance-based or equity-based; equity-based limits count floating losses and are much easier to breach.
- Static and trailing drawdown are fundamentally different products — know which one you are buying before you pay.
- Consistency, news, and weekend rules rarely appear in marketing pages but frequently appear in payout disputes; read the full terms.
- Rules change frequently. Verify current terms on the firm's official site before every evaluation attempt.
