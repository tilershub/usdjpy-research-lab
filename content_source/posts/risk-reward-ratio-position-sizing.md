---
title: "Risk-to-Reward Ratio and Position Sizing: How They Work Together"
excerpt: "Position sizing determines how much you risk. R:R ratio determines how much you can win. Most traders optimize one and ignore the other — here's how to combine them correctly."
published_at: "2026-04-30"
updated_at: "2026-04-30"
tags:
  - "R:R Ratio"
  - "Position Sizing"
  - "Risk Management"
  - "Forex"
  - "Trading Strategy"
primary_tag: "Risk Management"
meta_title: "Risk-to-Reward Ratio and Position Sizing — How They Work Together | TRADE90"
meta_description: "How R:R ratio and position sizing interact. Includes expected value formula, worked examples, and the correct order to calculate both. Free position size calculator."
reading_time: 9
author: "TRADE90"
---

Position sizing determines how much you risk. Your risk-to-reward ratio determines how much you can win. Most traders treat these as separate decisions — they're not. They're two sides of the same trade evaluation that must be assessed together before a single order is placed.

Here is the full picture.

---

## What Is Risk-to-Reward Ratio?

The risk-to-reward ratio (R:R) compares the potential loss on a trade to the potential gain. A 1:2 R:R means you risk $100 to potentially make $200. A 1:1 R:R means you risk and stand to gain the same amount.

```
R:R Ratio  = (Take Profit Distance) ÷ (Stop Loss Distance)
Dollar Risk = Account Balance × Risk %
Dollar Gain = Dollar Risk × R:R
```

A 1:2 R:R on a $10,000 account at 1% risk ($100) means a winning trade returns $200.

---

## Does R:R Ratio Change Your Position Size?

No — and this is the most common misconception. Your R:R ratio does not affect your lot size calculation. Position size is determined solely by:

1. Your account balance
2. Your risk percentage
3. Your stop loss distance (in pips)
4. The instrument pip value

The take profit level (which sets R:R) is separate. You calculate lot size from the stop, then set the take profit independently.

| What changes position size | What does NOT change position size |
|---|---|
| Account balance | Take profit level |
| Risk percentage (%) | R:R ratio |
| Stop loss distance (pips) | Confidence in the trade |
| Pip value per lot | Market session |

---

## The Correct Workflow: R:R First, Then Position Size

The professional order of operations before any trade:

**Step 1 — Identify the setup and confirm the stop loss level** (structural level, not arbitrary distance)

**Step 2 — Check the R:R ratio** — if target is less than 1.5× the stop distance, skip the trade

**Step 3 — Calculate position size** using the stop loss distance

**Step 4 — Enter the trade** with the correct lot size

Traders who skip Step 2 end up sizing into trades that can never produce good outcomes regardless of direction.

---

## Expected Value: Where R:R and Win Rate Combine

The reason R:R and position sizing must be considered together is expected value — the mathematical average outcome of a trade over a large sample.

```
Expected Value = (Win Rate × Dollar Reward) − (Loss Rate × Dollar Risk)
```

| Win Rate | R:R | EV per $100 risked | Profitable? |
|---|---|---|---|
| 40% | 1:1 | −$20 | No |
| 40% | 1:2 | +$40 | Yes |
| 50% | 1:1 | $0 | Breakeven |
| 50% | 1:2 | +$50 | Yes |
| 55% | 1:1 | +$10 | Yes |
| 60% | 1:1.5 | +$30 | Yes |
| 35% | 1:3 | +$45 | Yes |

A 35% win rate with 1:3 R:R is more profitable than a 55% win rate with 1:1 R:R. This is why both numbers must be known before sizing.

---

## Worked Example: EUR/USD Trade at 1:2 R:R

**Setup**: EUR/USD long, H1 timeframe  
**Account**: $10,000  
**Risk**: 1% = $100  
**Entry**: 1.08500  
**Stop Loss**: 1.08250 (25 pips below entry)  
**Take Profit**: 1.09000 (50 pips above entry)  
**R:R**: 50 ÷ 25 = **1:2**

```
Dollar Risk     = $10,000 × 1% = $100
Stop Loss Pips  = (1.08500 − 1.08250) ÷ 0.0001 = 25 pips
Lot Size        = $100 ÷ (25 × $10) = 0.40 lots
Dollar Gain     = $100 × 2 = $200 (if TP hit)
```

The position size is 0.40 lots. The R:R is 1:2. Both are determined before entry.

---

## What Happens When You Set TP Before Sizing

A common mistake: traders identify a 1:3 target and think they can use a smaller stop to "improve" R:R while maintaining the same lot size.

**Example of the trap**: EUR/USD long
- Real structural stop: 50 pips away
- Trader tightens stop to 20 pips to achieve 1:3 R:R on a 60-pip target
- Lot size at 1% risk, 20-pip stop: 0.50 lots
- Result: stop hits on normal intraday noise before price moves to target

The stop must be where the trade is structurally invalidated. R:R is the result of that structure — not something you engineer by manipulating the stop.

---

## R:R and Daily Risk Caps in Funded Accounts

For funded traders with a 1% daily risk cap (Trade90 Safety System), R:R ratio determines how many trades are needed to hit profit targets.

| Daily Risk Cap | Risk/Trade | Trades/Day | Win Rate | R:R | Expected Daily P&L |
|---|---|---|---|---|---|
| 1% ($1,000 on $100k) | 0.5% ($500) | 2 trades | 55% | 1:2 | +$50 avg |
| 1% ($1,000) | 0.5% ($500) | 2 trades | 50% | 1:2.5 | +$125 avg |
| 1% ($1,000) | 0.5% ($500) | 2 trades | 45% | 1:3 | +$175 avg |

Higher R:R trades require fewer wins per day to be profitable — critical when you're limited to 2 trades by the daily cap.

---

## Minimum Acceptable R:R by Strategy Type

Different trading styles require different minimum R:R thresholds to remain profitable:

| Strategy | Typical Win Rate | Minimum R:R for Profitability |
|---|---|---|
| Scalping | 60–70% | 1:0.8+ |
| Day trading | 45–55% | 1:1.5+ |
| Swing trading | 40–50% | 1:2+ |
| Position trading | 35–45% | 1:3+ |
| News trading | 30–40% | 1:4+ |

Never enter a day trade with R:R below 1:1.5. The math will not support profitability over time regardless of how good the setup looks.

---

## Using the TRADE90 Calculator for R:R + Position Size

The [TRADE90 position size calculator](/) calculates both R:R and lot size simultaneously when you enter entry, stop, and take profit levels:

1. Enter account balance and risk %
2. Enter entry price
3. Enter stop loss level
4. Enter take profit level
5. Read: lot size, dollar risk, R:R ratio, and risk state (Safe/Caution/Aggressive/Dangerous)

If the R:R shown is below 1:1.5, reconsider the trade before calculating further. The calculator flags trades where risk exceeds the daily cap.

---

## Frequently Asked Questions

**Does R:R ratio affect my lot size?**
No. Lot size is calculated from your risk percentage and stop loss distance only. R:R is a separate evaluation of trade quality — it does not change the lot size formula.

**What is a good risk-to-reward ratio for day trading?**
A minimum of 1:1.5, with 1:2 as the professional standard for most day trading styles. Below 1:1, you need a win rate above 50% just to break even after spreads.

**Can I trade with a 1:1 R:R?**
Yes, but you need a win rate consistently above 55% to profit after spread costs. Most retail traders cannot sustain that. 1:2 or higher is more forgiving.

**How do I calculate R:R ratio?**
Divide the take profit distance by the stop loss distance. If your stop is 30 pips and your target is 90 pips, R:R = 90 ÷ 30 = 1:3.

**Should I always use the same R:R?**
Not necessarily — R:R depends on market structure. Set your stop and target at structural levels, then check if the resulting R:R is acceptable. If it isn't, skip the trade rather than forcing the levels.
