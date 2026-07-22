---
title: "How to Pass the FTMO Challenge in 2026 — The Complete Strategy Guide"
excerpt: "The FTMO challenge has a reported pass rate of under 10%. This guide covers the exact rules, the most common failure points, and the risk management framework that separates funded traders from those who keep paying challenge fees."
published_at: "2026-04-05"
updated_at: "2026-04-05"
tags:
  - "FTMO"
  - "Funded Trading"
  - "Prop Firm"
  - "Challenge Strategy"
  - "Risk Management"
  - "Position Sizing"
primary_tag: "Funded Trading"
meta_title: "How to Pass the FTMO Challenge 2026 — Complete Strategy & Risk Rules | TRADE90"
meta_description: "The exact FTMO challenge rules, most common failure reasons, and the risk management framework that passes consistently. Includes position sizing strategy for the 0.5% rule. Free calculator."
reading_time: 11
author: "TRADE90"
---

FTMO's published pass rate sits below 10%. That is not a marketing statistic — it is the baseline reality of prop firm evaluations. Most traders don't fail because of bad strategy. They fail because of bad risk management applied to a decent strategy, compressing their edge into a single catastrophic drawdown event.

This guide covers the FTMO challenge rules in full, the exact failure modes that end evaluations, and the risk framework that passes them consistently.

---

## FTMO Challenge Rules — Everything That Can Fail You

Understanding what loses an evaluation is more important than understanding what wins one. Here are the hard rules that terminate a challenge immediately, regardless of how much profit is on the account.

### Phase 1 — The Challenge

| Rule | Requirement |
|---|---|
| Profit Target | +10% of initial account balance |
| Maximum Daily Loss | -5% of initial account balance |
| Maximum Total Drawdown | -10% of initial account balance |
| Minimum Trading Days | 4 calendar days |
| Time Limit | 30 calendar days |

**Maximum Daily Loss** is calculated from the previous day's ending balance, not the challenge start balance. If your account grows to $110,000 during the challenge, your daily loss limit for the following day is 5% of $110,000 = $5,500. It moves up with your balance — it does not move down.

**Maximum Total Drawdown** is calculated from the initial account balance. On a $100,000 challenge, the account must not fall below $90,000 — ever, under any circumstance, including overnight gaps.

### Phase 2 — The Verification

| Rule | Requirement |
|---|---|
| Profit Target | +5% of initial account balance |
| Maximum Daily Loss | -5% of initial account balance |
| Maximum Total Drawdown | -10% of initial account balance |
| Minimum Trading Days | 4 calendar days |
| Time Limit | 60 calendar days |

Phase 2 is identical to Phase 1 except the profit target drops to 5% and you have 60 days instead of 30. Traders who pass Phase 1 typically treat Phase 2 as routine — and that complacency is where many fail. The same rules apply. The same discipline is required.

---

## Why Traders Fail the FTMO Challenge — Data-Driven Analysis

Based on the patterns visible in funded trader forums and FTMO's own transparency reports, the top failure causes in order of frequency are:

### 1. Hitting the Daily Loss Limit (Most Common)

The 5% daily loss limit is the most common termination point. Here is how it happens:

A trader has a losing morning session — down 2.5% from two bad trades. Instead of stopping for the day, they enter a third trade trying to recover. That trade loses. They're now at 3.5% daily loss. Feeling the evaluation pressure, they increase position size on a fourth trade. That trade hits full stop. Evaluation terminated.

The mistake is not the first two losing trades. The mistake is the third trade taken in recovery mode with distorted judgment.

**Fix**: Set a personal daily loss limit of 1% — half the firm's 5% limit — and stop trading when you reach it. You will never hit the FTMO daily limit if you stop at 1%.

### 2. Oversizing — The Position Sizing Trap

Second most common failure mode. A trader uses 2% risk per trade, has a 3-trade losing streak, and is immediately at 6% total drawdown — over the 5% daily loss limit and approaching the 10% total limit simultaneously.

The mathematics are brutal:
- 2% risk × 5 consecutive losses = 10% drawdown → evaluation fails
- 1% risk × 5 consecutive losses = 5% drawdown → still inside limits
- 0.5% risk × 5 consecutive losses = 2.5% drawdown → comfortably inside limits

The only risk level that allows natural variance to occur without evaluation failure is 0.5%–1% maximum.

### 3. Running Positions Overnight or Through News

FTMO holds trades to their natural outcomes — including overnight gaps and major news events. A trade left open through a Non-Farm Payrolls release or a surprise central bank decision can gap 150+ pips in seconds. At 1% risk, a 150-pip stop may be $1,500 on a $100,000 account. At 2% risk with a 150-pip stop, that same gap is $3,000 — 3% of the account in a single candle.

**Fix**: Close positions before major news events. FTMO's news filter function (in the MT4/MT5 terminal) is not reliable enough to prevent slippage — manual close before news is the only safe approach.

### 4. Not Trading Enough Days

The minimum 4 trading days requirement catches traders who reach the profit target quickly (often in 2–3 large trades) and submit for review before hitting the minimum day count. The evaluation is automatically failed.

**Fix**: Track your trading day count alongside your profit. If you hit the profit target in 2 days, reduce size and continue trading defensively until you have 4 days logged.

### 5. Running Out of Time

30 days sounds like a long time. It is not, when you account for weekends (8–9 lost days), major holidays, and the reality that many traders only take 1–2 qualified setups per week. 30 calendar days often translates to 15–18 tradeable days.

**Fix**: Enter the challenge with a realistic trading frequency plan. If you trade 3 days per week, you have roughly 12 tradeable days. At 0.5% risk per trade with a 1:2 R:R ratio, you need 9 winning trades out of 12 to hit 10% profit — a 75% win rate requirement. Adjust your position sizing to account for the time constraint without compromising risk rules.

---

## The Risk Framework That Consistently Passes FTMO Challenges

The Trade90 Safety System applies two rules without exception:

**Rule 1: Maximum 0.5% risk per trade.**
At 0.5% per trade on a $100,000 challenge account, your maximum dollar risk per trade is $500. This allows 20 consecutive losses before hitting the 10% max drawdown. No strategy with a positive expected value produces 20 consecutive losses.

**Rule 2: Maximum 1% total risk per day.**
At 1% daily cap, you can have 2 trades open at once (each at 0.5%) before hitting your personal limit. When your daily risk allocation is used, stop trading. No exceptions. No "just one more" logic.

These two rules create a loss containment framework that is mathematically near-impossible to breach through normal trading variance.

---

## Position Sizing for the FTMO Challenge — Worked Examples

### $25,000 Challenge Account

| Risk Level | Dollar Risk Per Trade | Max Daily Loss (Personal) | Consecutive Losses to Fail |
|---|---|---|---|
| 0.5% | $125 | $250 | 20+ |
| 1.0% | $250 | $500 | 10 |
| 2.0% | $500 | $1,000 | 5 |

At 2% risk: 5 consecutive losses = $2,500 = 10% drawdown = **challenge failed**. This can happen in a single bad morning.

At 0.5% risk: 20 consecutive losses = $2,500 = 10% drawdown. A 20-trade losing streak at any edge-based strategy is a 1-in-a-million event.

### $100,000 Challenge Account

| Risk Level | Dollar Risk Per Trade | Trades to Reach 10% DD |
|---|---|---|
| 0.5% | $500 | 20 trades |
| 1.0% | $1,000 | 10 trades |
| 2.0% | $2,000 | 5 trades |

**To hit the 10% profit target with 0.5% risk at 1:2 R:R:**

- You need approximately 14 winning trades and 6 losing trades (70% win rate) to reach $10,000 profit
- Or 18 winning trades and 9 losing trades (66% win rate) — still achievable for a disciplined strategy
- The buffer against failure is 20 losses — more than enough room for a realistic loss rate

Use the [TRADE90 funded account calculator](/funded-trader-risk-calculator/) to model your specific scenario and instrument.

---

## FTMO Rules That Catch People Off Guard

### The Equity Stop vs. Balance Stop Distinction

FTMO uses **equity** for drawdown calculations, not balance. This means:
- A trade that is currently $800 unrealized loss counts toward your daily limit — even if you haven't closed it
- If you have two open trades simultaneously, both unrealized losses combine against your daily limit
- You can breach the daily loss limit with open positions, even without a stop-out

**Fix**: Count your total exposure (open + closed) against the daily limit at all times. The TRADE90 daily risk tracker includes open risk in the calculation.

### The "From Previous Day's Balance" Daily Loss Rule

Your daily loss limit resets each midnight (server time) based on the previous session's closing balance, not the original challenge balance. If you had a profitable day and closed at $103,000, tomorrow's daily loss limit is 5% of $103,000 = $5,150.

This means a profitable run actually widens your absolute dollar loss limit — but you should still measure against your personal 1% cap, not FTMO's 5% cap.

### Weekend and Overnight Gap Risk

FTMO does not close your positions over the weekend. If you hold trades through the Friday close, gap risk is entirely yours. In periods of high geopolitical uncertainty (elections, central bank emergency meetings, major economic crises), weekend gaps on gold, indices, or currency pairs can exceed 200+ pips.

Close positions before the Friday close if there is any meaningful uncertainty in the macro environment.

---

## FTMO Instruments — Which Are Best for Challenge Passing?

The best instruments for FTMO challenges are those with:
- Clear technical structure (reduces strategy edge variance)
- Tight spreads (reduces friction against your profit target)
- High liquidity (reduces slippage on stops)

**Recommended challenge instruments:**

| Instrument | Why It Works | Position Sizing Note |
|---|---|---|
| EUR/USD | Tightest spreads, cleanest technicals | $10/pip standard lot |
| GBP/USD | Strong directional moves, clear levels | $10/pip standard lot |
| XAUUSD (Gold) | High ADR, great R:R potential | $10/pip, wider stops needed |
| NAS100 | Strong trending behavior | $1/point, requires index sizing |
| US30 | Clear support/resistance | $1/point |

Avoid exotic pairs on challenges — wide spreads eat directly into your 10% profit target.

---

## A Realistic FTMO Challenge Timeline

Assuming you take 3 qualified setups per week at 0.5% risk:

**Week 1**: 3 trades. Best-case 2 wins, 1 loss = +0.5% net. Account: $100,500.
**Week 2**: 3 trades. 2 wins, 1 loss = +0.5% net. Account: $101,000.
**Week 3**: 4 trades (extra setup). 3 wins, 1 loss = +1.0% net. Account: $102,000.
**Week 4**: 4 trades. 3 wins, 1 loss = +1.0% net. Account: $103,000.

That is a conservative, realistic path to 3% profit in 30 days — not the 10% target. To hit 10%, you need either:
- A higher win rate (75%+)
- A better average R:R (closer to 1:3)
- More setups per week (5–6 per week is sustainable)
- Or some combination of all three

The point is: 10% in 30 days at 0.5% risk is achievable — it requires consistent execution, not a single large winning trade.

---

## Free Tools for FTMO Challenge Preparation

Before starting an FTMO challenge, use these free tools to calibrate your sizing:

- **[FTMO Position Size Calculator](/ftmo-position-size-calculator/)** — sizing tool optimized for FTMO challenge parameters
- **[Funded Trader Risk Calculator](/funded-trader-risk-calculator/)** — full Trade90 Safety System with daily risk tracker
- **[EUR/USD Calculator](/calculator/eurusd/)** — most popular FTMO instrument
- **[XAUUSD Calculator](/calculator/xauusd/)** — gold-specific sizing with wide stop support

Calculate your exact lot size before every single trade. No exceptions. No mental math on a live chart.

---

## Frequently Asked Questions

**What is the FTMO challenge pass rate?**
FTMO has stated the overall pass rate is approximately 8–10% of all challenge attempts. The failure rate is high not because the rules are strict but because most traders don't apply consistent risk management during the evaluation period.

**Can you trade news on FTMO?**
Yes, FTMO allows trading during news events. However, trading into major news events (Non-Farm Payrolls, FOMC, CPI) exposes your positions to extreme slippage. Most experienced funded traders exit positions before major news rather than holding through them.

**What happens if you fail the FTMO challenge?**
FTMO offers a free retry on their Challenge account type if you trade for at least 10 days and don't breach the loss limits. If you breach the daily or total loss limit, you must purchase a new challenge.

**How many trades do you need to pass the FTMO challenge?**
There is no minimum trade count beyond the 4-day minimum. In theory, you could pass with 4–8 well-executed trades if the R:R is high enough. In practice, most traders need 15–25 trades to reach the 10% target with acceptable variance.

**Is FTMO worth it for US traders?**
Yes — FTMO accepts US traders and is one of the few major prop firms that has maintained consistent US access. Their payout record and operational history make them a reliable option compared to newer firms. See the [best prop firms for US traders](/best-prop-firms-usa/) guide for a full comparison.
