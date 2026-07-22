---
title: "The 1% Position Sizing Rule Explained — Why It Protects Your Trading Account"
excerpt: "The 1% rule is the most cited risk management principle in trading — and the most misunderstood. This guide breaks down exactly what it means, the math behind it, and how to apply it to every trade you take."
published_at: "2026-04-28"
updated_at: "2026-04-28"
tags:
  - "1% Rule"
  - "Risk Management"
  - "Position Sizing"
  - "Forex"
  - "Trading Rules"
primary_tag: "Risk Management"
meta_title: "The 1% Position Sizing Rule Explained — Why It Protects Your Account | TRADE90"
meta_description: "What is the 1% position sizing rule? Full explanation, formula, and examples for forex & funded traders. Free calculator included."
reading_time: 9
author: "TRADE90"
---

Ask any experienced trader what rule beginners should follow first, and the answer is almost always the same: never risk more than 1% of your account on a single trade. Yet studies of retail trading accounts consistently show that the majority of losing traders were risking between 5% and 20% per trade right before they blew up. The rule is everywhere. The understanding of it is not.

This guide explains exactly what the 1% position sizing rule means, why 1% specifically is the right number, and how to apply it with a real formula across different instruments and account sizes.

---

## What the 1% Rule Actually Means

The 1% rule is simple but specific: **you risk no more than 1% of your total account balance on any single trade.**

This is a dollar risk limit, not a lot size limit. It is calculated from your account balance and your stop loss distance — not from the size of the position alone.

If your account is $10,000, your maximum dollar risk per trade is $100. If your stop loss is hit on that trade, you lose exactly $100 — not a cent more. Your position size is then calculated backward from that $100 figure, depending on the instrument, pip value, and stop loss distance.

This is where traders misunderstand the rule. Many assume "1% risk" means trading 0.01 lots, or that it means limiting their position to 1% of their account in notional value. It means neither of those things. It means the maximum amount you can lose if your stop loss is triggered is 1% of your current account balance.

---

## The Formula

Every position size calculation under the 1% rule uses the same core formula:

```
Dollar Risk = Account Balance × Risk Percentage
Lot Size = Dollar Risk ÷ (Stop Loss in Pips × Pip Value per Lot)
```

For a standard forex pair where 1 standard lot = $10 per pip:

```
Lot Size = (Account Balance × 0.01) ÷ (Stop Loss Pips × 10)
```

For gold (XAUUSD), where 1 standard lot = $10 per pip (but pip = $0.01, so $1,000 per $1 move per lot — typically $1 per pip per 0.01 lot):

```
Lot Size = (Account Balance × 0.01) ÷ (Stop Loss in USD × 100)
```

Use the [TRADE90 position size calculator](/) to handle these calculations automatically across all instruments without manual arithmetic.

---

## Dollar Risk at 1% — Account Size Reference Table

The first step in applying the 1% rule is knowing your maximum dollar risk figure. This is your hard limit for every trade:

| Account Balance | 1% Max Risk per Trade |
|---|---|
| $1,000 | $10 |
| $5,000 | $50 |
| $10,000 | $100 |
| $25,000 | $250 |
| $50,000 | $500 |
| $100,000 | $1,000 |
| $200,000 | $2,000 |

These numbers scale linearly. As your account grows through profitable trading, your dollar risk per trade increases proportionally — which is exactly how compounding is supposed to work.

---

## Why 1% Specifically — The Losing Streak Math

The reason traders use 1% rather than 2% or 5% is not arbitrary. It comes from the mathematics of losing streaks and account survival.

Every trader — even profitable ones — experiences strings of consecutive losses. A strategy with a 50% win rate will produce runs of 5, 6, or 7 consecutive losses with regularity over a trading career. The question is how much capital survives those runs.

The table below shows account balance remaining after 10 consecutive losses at different risk percentages, starting with a $10,000 account:

| Risk per Trade | After 5 Losses | After 10 Losses | After 20 Losses |
|---|---|---|---|
| 1% | $9,510 | $9,044 | $8,179 |
| 2% | $9,039 | $8,171 | $6,676 |
| 5% | $7,738 | $5,987 | $3,585 |
| 10% | $5,905 | $3,487 | $1,216 |
| 20% | $3,277 | $1,074 | $115 |

At 1% risk, 10 consecutive losses leave you with over 90% of your account intact. You need only a few winning trades to recover. At 5% risk, 10 losses cut your account nearly in half. At 10%, you have lost two-thirds of your capital and face a 200% return requirement just to break even.

This is why 1% is the professional standard. It is not conservative — it is mathematically rational.

---

## The 1% Rule for Funded Accounts vs Retail Accounts

The 1% rule applies differently depending on whether you are trading your own capital or a funded prop firm account.

**Retail accounts:** 1% is the maximum. Many experienced traders use 0.5–0.75% as their standard and reserve 1% for the highest-conviction setups only.

**Funded accounts (FTMO, Apex, The5ers, etc.):** The professional standard drops to **0.5% per trade**. Funded accounts carry daily drawdown limits — typically 4–5% — and maximum drawdown limits of 8–10%. At 1% risk per trade, a single bad day of 4 losing trades consumes your entire daily allowance and puts your account at serious risk. At 0.5%, four losing trades cost 2% — uncomfortable but recoverable.

Funded traders who use 1% are playing with half the margin for error that the challenge rules allow. Most traders who fail funded accounts do so because they treated the challenge capital like personal money and sized accordingly.

For prop firm accounts, consider 0.5% your hard ceiling and 0.25–0.5% your working range. See the [prop firm risk management guide](/prop-firm-risk-management/) for the complete funded account framework.

---

## How to Calculate Lot Size from the 1% Rule — Worked Examples

### EUR/USD Example

- Account: $10,000
- Risk: 1% = $100
- Stop loss: 50 pips
- Pip value (EUR/USD, standard lot): $10 per pip

```
Lot Size = $100 ÷ (50 pips × $10) = $100 ÷ $500 = 0.20 lots
```

A 0.20 lot position with a 50-pip stop on EUR/USD risks exactly $100, which is 1% of a $10,000 account.

### Gold (XAUUSD) Example

- Account: $10,000
- Risk: 1% = $100
- Stop loss: $5.00 (500 pips in gold notation)
- Pip value (XAUUSD, 0.01 lot): $0.10 per pip

```
Lot Size = $100 ÷ (500 pips × $0.10) = $100 ÷ $50 = 2.00 lots
```

Wait — that cannot be right for a $10,000 account. This is where gold catches traders. In standard lot notation, 1.00 lot of XAUUSD = $100 per pip (where 1 pip = $0.01). So:

```
Lot Size = $100 ÷ ($5.00 stop × $100 per lot per dollar) = $100 ÷ $500 = 0.20 lots
```

The [TRADE90 position size calculator](/) handles gold pip value automatically — use the XAUUSD preset rather than calculating manually. The instrument-specific pip values are pre-loaded.

---

## When to Go Below 1%

The 1% rule is a ceiling, not a target. There are specific market conditions where dropping to 0.25–0.5% per trade is the correct decision:

**High-volatility periods:** During major news events (FOMC, NFP, CPI), spreads widen, slippage occurs, and stop losses are more likely to be triggered at worse levels than intended. Reducing risk by 50% before news events is standard practice among professional traders.

**Unclear market structure:** When price is in a range with no clear structure, or when higher timeframe direction conflicts with your entry timeframe, the trade carries more uncertainty. Lower risk reflects that uncertainty accurately.

**Learning phase on a new instrument:** If you have never traded NAS100 and you are used to forex, the first 20–30 trades on the new instrument should be at 0.25% risk. Volatility characteristics, pip values, and correlation patterns are different. Reduced size lets you learn without significant financial consequence.

**Small accounts under $2,000:** At 1% risk on a $1,000 account, your maximum dollar risk is $10. This forces extremely small positions that may not be available on all brokers. Many micro-account traders use a fixed $5–$10 risk per trade rather than a strict percentage while building capital.

---

## Common 1% Rule Misconceptions

**Misconception 1: The 1% rule means my profit target is 1%**
The 1% rule describes your maximum LOSS, not your profit target. Your profit target is determined by your risk-to-reward ratio — a 1:2 R:R trade risking 1% should target 2% gain.

**Misconception 2: The 1% rule applies per day, not per trade**
The rule applies per trade. Some traders layer a separate daily loss limit of 2–3% on top of the per-trade rule, but those are distinct concepts. Each individual trade is capped at 1%.

**Misconception 3: 1% risk means 1% of account in position size**
A $10,000 account with 1% risk does not mean your position is worth $100. On a 50-pip stop with EUR/USD, your 0.20 lot position is worth $20,000 in notional value — but your RISK (the amount lost at stop) is $100.

**Misconception 4: The 1% rule is only for beginners**
Professional prop traders, hedge fund managers, and institutional traders all operate with maximum single-trade risk limits. 1% or less is the standard for anyone managing significant capital seriously.

**Misconception 5: You cannot make meaningful money with 1% risk**
At $100,000 with 1% risk and a 1:2 R:R, 10 winning trades at $1,000 each produce $10,000 in profit — a 10% return. The compounding effect of consistent 1% risk management on a growing account is substantial over 12–24 months.

---

## Applying the 1% Rule With a Calculator

Manual calculation is error-prone, especially under the time pressure of live markets. The sequence is:

1. Check your current account balance
2. Multiply by 0.01 to get your dollar risk
3. Identify your stop loss in pips (or dollars for gold/indices)
4. Divide dollar risk by (stop pips × pip value)

A dedicated calculator removes human error from this process entirely. Use the [TRADE90 position size calculator](/) before entering every trade — input your balance, risk percentage, stop loss, and instrument, and get the exact lot size in seconds.

For a deeper analysis of how to determine the right risk percentage for your specific account and strategy, read [How Much Should I Risk Per Trade?](/blog/how-much-should-i-risk-per-trade/).

---

## FAQ

**What is the 1% rule in trading?**

The 1% rule states that you should never risk more than 1% of your total trading account balance on any single trade. If your account is $20,000, the maximum you should be willing to lose on one trade is $200. Your position size is then calculated from this dollar risk figure, your stop loss distance, and the instrument's pip value.

**Should I use 0.5% or 1% risk?**

It depends on your account type and trading context. For retail traders with a solid strategy, 1% is appropriate for standard conditions. For funded prop firm accounts, 0.5% is the professional standard because daily drawdown limits make 1% risk unsustainable across multiple trades in a losing day. During high-volatility events or when learning a new instrument, 0.25–0.5% is the right range.

**How do I apply the 1% rule?**

Multiply your account balance by 0.01 to find your dollar risk. Then calculate: Lot Size = Dollar Risk ÷ (Stop Loss in Pips × Pip Value per Standard Lot). For EUR/USD with a $10,000 account and 40-pip stop: $100 ÷ (40 × $10) = 0.25 lots. Use a position size calculator to automate this step.

**Does the 1% rule guarantee profits?**

No. The 1% rule is a capital preservation tool, not a profit strategy. It ensures that losing streaks — which every trader experiences — do not destroy your account before your edge has time to play out. A trader with a profitable strategy but poor risk management will still lose. A trader with a break-even strategy and perfect risk management will still not profit. Both are required.

**Is the 1% rule good for beginners?**

Yes, but beginners should consider starting at 0.25–0.5% while they are learning. The psychological pressure of real money — even at 1% — can cause beginners to move stop losses, exit trades early, or over-trade. Reducing the dollar amount at risk reduces the emotional stakes while the skill foundation is being built. Once your win rate and process are consistent over 3 months, step up to 1%.
