---
title: "NAS100 Position Size Calculator — Complete Lot Size Guide for Funded Traders"
excerpt: "NAS100 (Nasdaq 100) is one of the most popular indices on prop firm funded accounts. This guide covers the exact point value formula, position sizing at every account level, and why Nasdaq requires different risk management than forex."
published_at: "2026-04-15"
updated_at: "2026-04-15"
tags:
  - "NAS100"
  - "Nasdaq"
  - "Indices Trading"
  - "Position Sizing"
  - "Funded Trading"
  - "Prop Firm"
  - "Lot Size Calculator"
primary_tag: "Indices Trading"
meta_title: "NAS100 Position Size Calculator — Lot Size Guide for Funded Traders 2026 | TRADE90"
meta_description: "How to calculate your NAS100 lot size for funded prop firm accounts. Full point value formula, worked examples, daily range context, and the 0.5% rule applied to Nasdaq. Free calculator."
reading_time: 9
author: "TRADE90"
---

NAS100 is not a forex pair. It doesn't pip at $10 per standard lot. It doesn't have consistent daily ranges you can memorize once. The Nasdaq 100 is a live, daily-repriced index driven by earnings surprises, Fed policy, and tech sector sentiment — and it moves in ways that can end a funded evaluation in a single session if you aren't sizing correctly.

This guide covers everything you need to size NAS100 positions correctly: the point value formula, how to translate index points to dollar risk, worked examples at every common funded account level, and the key differences between trading NAS100 vs. forex on a prop firm evaluation.

---

## NAS100 vs. Forex: The Key Differences for Position Sizing

**1. Points, not pips.**
NAS100 is priced in index points, not currency pips. As of 2026, the Nasdaq 100 trades around 18,000–22,000 points. A "1-point" move is the smallest price increment — the equivalent of a pip for forex.

**2. Variable point value.**
Unlike EUR/USD where 1 pip = $10 per standard lot regardless of price level, the dollar value of a 1-point NAS100 move depends on your broker's contract specification. Most retail and prop firm brokers use a contract size of **$1 per point per lot** for NAS100 (also called US100, USTEC, or NDX depending on the platform).

**3. Wide daily ranges.**
NAS100's average daily range is 150–300+ points in normal conditions, and can exceed 500–800 points during major tech earnings or Fed announcement days. A 100-point stop that feels "wide" on a chart is actually on the conservative side for Nasdaq.

**4. Gap risk.**
Nasdaq can gap significantly on pre-market earnings reports from major components (Apple, Microsoft, Nvidia, Meta, Amazon, Google). These gaps appear overnight and on Sunday opens and cannot be stopped out at your stated stop loss.

---

## The NAS100 Point Value Formula

For most brokers and prop firm platforms, NAS100 has this contract structure:

- **1 standard lot** = $1 per point movement
- **0.10 lots (mini)** = $0.10 per point movement
- **0.01 lots (micro)** = $0.01 per point movement

```
Dollar Risk  = Stop Loss (points) × $1 × Lot Size
Lot Size     = Dollar Risk ÷ (Stop Loss Points × $1)
```

**Example at $100,000 account, 0.5% risk, 100-point stop:**
```
Dollar Risk  = $100,000 × 0.5% = $500
Lot Size     = $500 ÷ (100 × $1) = 5.00 lots
```

**Note on broker variations**: Some brokers quote NAS100 with a contract size of $10 per point per lot (similar to the CME Nasdaq E-mini futures). Always verify your broker's contract specification before trading. The TRADE90 NAS100 calculator uses the standard $1-per-point specification used by most prop firm brokers.

---

## NAS100 Lot Size Tables — All Account Sizes

The following examples use **0.5% risk per trade** — the Trade90 Safety System maximum for funded accounts.

### $10,000 Account — 0.5% Risk = $50

| Stop Loss (points) | Lot Size | Dollar Risk |
|---|---|---|
| 30 points | 1.67 lots | $50 |
| 50 points | 1.00 lot | $50 |
| 80 points | 0.63 lots | $50 |
| 100 points | 0.50 lots | $50 |
| 150 points | 0.33 lots | $50 |
| 200 points | 0.25 lots | $50 |

### $25,000 Account — 0.5% Risk = $125

| Stop Loss (points) | Lot Size | Dollar Risk |
|---|---|---|
| 30 points | 4.17 lots | $125 |
| 50 points | 2.50 lots | $125 |
| 100 points | 1.25 lots | $125 |
| 150 points | 0.83 lots | $125 |
| 200 points | 0.63 lots | $125 |

### $50,000 Account — 0.5% Risk = $250

| Stop Loss (points) | Lot Size | Dollar Risk |
|---|---|---|
| 50 points | 5.00 lots | $250 |
| 80 points | 3.13 lots | $250 |
| 100 points | 2.50 lots | $250 |
| 150 points | 1.67 lots | $250 |
| 200 points | 1.25 lots | $250 |

### $100,000 Account — 0.5% Risk = $500

| Stop Loss (points) | Lot Size | Dollar Risk |
|---|---|---|
| 50 points | 10.00 lots | $500 |
| 100 points | 5.00 lots | $500 |
| 150 points | 3.33 lots | $500 |
| 200 points | 2.50 lots | $500 |
| 300 points | 1.67 lots | $500 |

### $200,000 Account — 0.5% Risk = $1,000

| Stop Loss (points) | Lot Size | Dollar Risk |
|---|---|---|
| 100 points | 10.00 lots | $1,000 |
| 150 points | 6.67 lots | $1,000 |
| 200 points | 5.00 lots | $1,000 |
| 300 points | 3.33 lots | $1,000 |

---

## What Stop Loss Distance to Use on NAS100

This is the question that trips up most traders moving from forex to indices. There is no universal "right" stop — but there are useful frameworks based on timeframe and market structure.

### By Timeframe

| Trading Style | Typical Valid Stop | Notes |
|---|---|---|
| Scalp (M1–M5) | 20–50 points | Requires fast execution, tight spread |
| Intraday (M15–H1) | 60–150 points | Most common for funded traders |
| Swing (H4–D1) | 200–500 points | Lower frequency, higher R:R potential |

### By Market Condition

| Condition | Recommended Minimum Stop |
|---|---|
| Low-volatility session (overnight Asia) | 50–80 points |
| Normal London/New York session | 80–150 points |
| High-volatility (FOMC, major earnings) | 200+ points or flat |

The most common mistake on NAS100 is using forex-sized stops (30–50 points) on an instrument with a 200+ point daily range. A 30-point stop will be hit by normal intraday noise on nearly every trade — leading to a sequence of small losses that accumulate into a meaningful drawdown before you've had a chance to capture a winning trade.

---

## NAS100 vs. US30 vs. SPX500 — Choosing Your Index

Funded traders commonly trade all three major US indices. Here's how they compare for position sizing purposes:

| Index | Daily Range (typical) | Volatility Profile | Best For |
|---|---|---|---|
| NAS100 | 150–350 points | High — tech-driven | Trending markets, breakouts |
| US30 (Dow) | 200–400 points | Moderate — blue-chip | Range trading, slower trends |
| SPX500 | 20–50 points | Lower relative — broad market | Lower-leverage approaches |

**Important**: SPX500 has a different scale — it trades around 4,500–5,500 points, and a 20-point daily range is normal. The pip value per lot on SPX500 is typically $1 per point, same as NAS100, but the absolute point ranges are much smaller.

For funded traders on 2-phase evaluations (like FTMO), NAS100's stronger trending behavior and clear technical breakpoints make it well-suited for building consistent 1:2–1:3 R:R setups. The key is using a stop loss wide enough to survive the noise.

---

## The NAS100 and the Daily Risk Cap

At 1% daily risk cap (Trade90 Safety System), a $100,000 funded account can deploy a maximum of $1,000 in daily risk across all NAS100 positions.

With 0.5% per trade ($500 risk each), you have **2 trades per day** before reaching the cap. For NAS100, this is actually sufficient — the index produces 2–4 high-probability setups per session on most days, and taking only the best 2 preserves both the daily cap and your psychological composure.

Traders who take 6–8 Nasdaq trades per day are almost always overtrading — filling time between genuine setups with low-probability entries. The transaction costs and spread alone reduce the expected value of high-frequency index trading.

---

## NAS100 Position Sizing: Special Scenarios

### Trading Earnings Season on NAS100

The Nasdaq 100 is heavily weighted toward mega-cap tech stocks. When Apple, Nvidia, Microsoft, or Google reports earnings after hours, NAS100 can gap 100–300 points overnight. During earnings season (January, April, July, October), funded traders should:

1. Reduce position size to 0.25% risk per trade
2. Close positions before the close of the day preceding major component earnings
3. Re-enter only after the gap has been absorbed and new structure is visible

A 300-point overnight gap at standard sizing can breach a funded account's daily loss limit in a single candle — without any ability to exit at your stop.

### FOMC Days

Federal Reserve meeting days (8 per year, plus additional communications) are the single highest-risk days for NAS100 positions. The Fed's rate decision and commentary directly impacts tech valuations, and the market's reaction can be 400–600 points in either direction within 30 minutes.

**Best practice**: Close all NAS100 positions at least 30 minutes before the FOMC announcement. Re-enter only after the initial volatility has settled and a clear directional trend is established.

### The VIX Relationship

NAS100 moves inversely to the VIX (volatility index) most of the time. When VIX is elevated (above 20), NAS100 intraday ranges expand significantly. During high-VIX periods, expand your stop loss distance proportionally and reduce lot size to maintain the same dollar risk.

---

## How to Use the NAS100 Position Size Calculator

The [TRADE90 NAS100 calculator](/calculator/nas100/) automatically applies the $1-per-point specification used by major prop firm brokers.

**Step 1**: Enter your account balance.

**Step 2**: Enter your risk percentage (0.5% for funded accounts, 1% maximum).

**Step 3**: Enter your entry price. For NAS100, this is the index level at your planned entry (e.g., 19,450).

**Step 4**: Enter your stop loss level (e.g., 19,300 for a 150-point stop below entry on a long trade).

**Step 5**: Read the lot size output. This is the position size to enter in your broker's order window.

The calculator also shows your Risk:Reward ratio if you enter a take profit level — which helps you avoid entering trades with negative expectancy before you've placed the order.

---

## Frequently Asked Questions

**What is 1 lot on NAS100?**
On most prop firm and retail broker platforms, 1 standard lot of NAS100 controls a position where each 1-point move is worth $1.00. A 100-point move against a 1-lot position would result in a $100 gain or loss.

**What is the pip value for NAS100?**
NAS100 uses "points" rather than pips. Most brokers set the contract value at $1 per point per lot. A 50-point stop on a 2-lot position risks $100 (50 points × $1 × 2 lots).

**What lot size for NAS100 on a $10,000 account?**
At 0.5% risk ($50) with a 100-point stop: Lot Size = $50 ÷ (100 × $1) = 0.50 lots. Use the [NAS100 position size calculator](/calculator/nas100/) to compute this instantly for any stop distance.

**Can you trade NAS100 on FTMO?**
Yes. NAS100 (listed as US100 on FTMO's platform) is a supported instrument on all FTMO account types. It is one of the most popular funded trading instruments due to its strong trending behavior and liquidity.

**What time does NAS100 trade?**
NAS100 trades 24 hours from Sunday 11pm UTC to Friday 10pm UTC with a brief break. The highest-liquidity, lowest-spread sessions are during US market hours (13:30–21:00 UTC). Avoid trading NAS100 during the Asian session unless you are an experienced index trader — the overnight session has wider spreads and lower liquidity.

**Is NAS100 or gold better for prop firm challenges?**
Both are popular and viable. Gold (XAUUSD) offers clearer technical structure and lower correlation to US macro data. NAS100 offers stronger trending behavior and better intraday setups during US hours. Many funded traders use both — gold in the London session and Nasdaq during the US session. See the [XAUUSD lot size guide](/blog/gold-lot-size-calculator-guide/) for a full gold position sizing reference.
