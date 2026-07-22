---
title: "Position Sizing Formula: The Complete Mathematical Guide for Every Market"
excerpt: "One formula works for forex, gold, indices, and crypto. Most traders memorize a rule of thumb instead of understanding the math — this guide shows you the full calculation for every instrument type."
published_at: "2026-04-25"
updated_at: "2026-04-25"
tags:
  - "Position Sizing"
  - "Formula"
  - "Risk Management"
  - "Forex"
  - "Lot Size"
primary_tag: "Position Sizing"
meta_title: "Position Sizing Formula: Complete Mathematical Guide for Every Market | TRADE90"
meta_description: "The complete position sizing formula for forex, gold, indices, and crypto. Worked examples, pip value tables, and a free calculator for every instrument."
reading_time: 10
author: "TRADE90"
---

There is one position sizing formula that works for every market — forex, gold, indices, and cryptocurrency. Most traders either don't know it or replace it with a rule of thumb like "I always trade 0.10 lots." The rule of thumb is why their risk per trade varies by 500% from one trade to the next, and why they never understand why some losing streaks destroy accounts while others barely make a dent.

This guide breaks down the universal position sizing formula, shows how pip value adapts across instrument types, and walks through real worked calculations for EUR/USD, XAUUSD, NAS100, and GBP/JPY — including the specific numbers that change for each market.

---

## The Universal Position Sizing Formula

```
Dollar Risk  = Account Balance × (Risk % ÷ 100)
Pip Value    = (Instrument-specific — see tables below)
Lot Size     = Dollar Risk ÷ (Stop Loss Distance × Pip Value per Standard Lot)
```

These three lines apply to every market. The only variable that changes between instruments is the pip value in line 2. Once you understand how to calculate the pip value for any instrument, you can size positions correctly across every market you trade.

The [TRADE90 position size calculator](/) applies this formula automatically for all major instruments, including gold, NAS100, and JPY pairs where the pip value calculation requires extra steps.

---

## Breaking Down Each Component

### Component 1: Dollar Risk

Dollar Risk is the maximum amount of money you're willing to lose on this specific trade. It is derived entirely from your account balance and your chosen risk percentage.

At $15,000 account balance with 1% risk: Dollar Risk = $150.  
At $15,000 account balance with 0.5% risk: Dollar Risk = $75.

This number must be calculated on your *current* balance every session — not your starting balance from three months ago. As your account grows, your dollar risk grows proportionally. As it shrinks after losses, your dollar risk decreases automatically, reducing position sizes and providing a natural brake against compounding losses.

### Component 2: Stop Loss Distance

The stop loss distance is the number of pips (or points) from your entry to your stop. This must be determined by the market structure of the trade — where the setup is invalidated — not by a dollar amount you're comfortable losing.

Common mistake: setting the stop based on a desired lot size. The correct sequence is always: (1) find the structurally valid stop, (2) calculate the lot size for that stop.

### Component 3: Pip Value

Pip value is where most traders' understanding breaks down. It varies by instrument, broker contract specification, and for some currencies, current exchange rates. The sections below cover each instrument category.

---

## Pip Value Formula by Instrument Type

### Major Forex Pairs (USD-Quoted)

For EUR/USD, GBP/USD, AUD/USD, NZD/USD — any pair where USD is the quote currency:

```
Pip Value = Pip Size × Lot Size × Contract Size
          = 0.0001 × 1.00 × 100,000 = $10.00 per pip per standard lot
```

This is constant and does not change with price levels. One pip on EUR/USD is always $10 per standard lot.

### JPY Pairs

For USD/JPY, EUR/JPY, GBP/JPY — pairs where JPY is the quote currency:

```
Pip Value = (Pip Size ÷ Current USD/JPY Rate) × Contract Size
          = (0.01 ÷ 150.00) × 100,000 ≈ $6.67 per pip per standard lot
```

The pip value for JPY pairs changes as USD/JPY moves. At USD/JPY = 140, pip value ≈ $7.14. At USD/JPY = 160, pip value ≈ $6.25. Most brokers and calculators update this automatically.

### Gold / Metals (XAUUSD)

```
Pip Value = Pip Size × Lot Size × Contract Size (troy oz)
          = 0.01 × 1.00 × 100 oz = $1.00 per pip... × 10 = $10.00
```

Wait — the confusing part. Gold's pip size is $0.01 (a price move from $2,300.00 to $2,300.01). One standard lot of XAUUSD = 100 troy ounces. So: 0.01 × 100 = $1.00? No — the pip is $0.01, the contract is 100 oz, meaning each $0.01 price move = $0.01 × 100 oz = $1.00, and that $1.00 move is 1 pip. Brokers display gold pricing with 2 decimal places, so a move from $2,300.00 to $2,301.00 = 100 pips, each worth $1.00 × lot size. Per standard lot: $10.00 per pip (since 100 pips × $1.00 = $100 per full dollar move, or equivalently, each "pip" = $10 × lot size when using the broker's pip scale). Always verify with your broker.

**Practical XAUUSD pip value**: $10.00 per pip per standard lot (the same as EUR/USD).

### Indices (NAS100, US30, SPX500)

```
Dollar Value = Points × Contract Value per Point × Lot Size
```

Most prop firm and retail broker platforms price NAS100 (US100) as:

```
$1.00 per point per lot
```

So a 100-point stop on 1.00 lot NAS100 = $100 risk. Some brokers price it at $10/point (similar to CME E-mini futures) — always verify in your broker's contract specifications.

### Cryptocurrency (BTC, ETH)

Crypto CFD contracts vary widely by broker. A common structure is:

```
Contract Size = 1 BTC (or 1 ETH) per lot
Dollar Risk   = Price Move × Lot Size
```

At BTC priced at $70,000, a 500-point ($500) stop on 0.10 lot BTC = $500 × 0.10 = $50 risk. Crypto pip values effectively equal the price move in USD since BTC is quoted in USD.

---

## Formula Application Table: Four Instruments Compared

This table shows exactly how the same formula adapts across four different instruments for a $20,000 account at 1% risk ($200 dollar risk):

| Instrument | Entry | Stop | SL Distance | Pip Value | Lot Size |
|---|---|---|---|---|---|
| EUR/USD | 1.0850 | 1.0780 | 70 pips | $10/pip | 0.29 lots |
| XAUUSD | 2,310.00 | 2,260.00 | 500 pips | $10/pip | 0.04 lots |
| GBP/JPY | 188.50 | 187.00 | 150 pips | $6.67/pip | 0.20 lots |
| NAS100 | 19,500 | 19,350 | 150 points | $1/point | 1.33 lots |

Note: GBP/JPY uses USD/JPY ≈ 150 for pip value calculation. NAS100 uses $1/point broker contract.

---

## The Kelly Criterion vs. Fixed Percentage

The Kelly Criterion is a mathematical formula that calculates the theoretically optimal fraction of capital to risk per trade to maximize long-run growth:

```
Kelly % = Win Rate – (Loss Rate ÷ Reward:Risk Ratio)
```

For a strategy with 55% win rate and 1:1.5 R:R: Kelly % = 0.55 – (0.45 ÷ 1.5) = 0.55 – 0.30 = 25%.

That 25% figure is the mathematical maximum — in practice, it produces enormous drawdowns and is psychologically untenable for most traders. Most practitioners use half-Kelly or quarter-Kelly, which for the above strategy would be 6–12%.

**Why fixed percentage wins in practice**: Fixed % (1% per trade) requires no edge estimation, adapts automatically to account size changes, and caps maximum drawdown across known loss streak lengths. Kelly requires accurate win rate and R:R estimation — which changes over time and is nearly impossible to measure precisely in real-time trading conditions.

For most traders, 0.5–1% fixed risk per trade outperforms Kelly variants because the simplicity eliminates a major source of error.

---

## Worked Calculation: EUR/USD Trade (Step by Step)

**Setup**: Long EUR/USD trade. You identify a bullish pin bar at the 1.0800 support zone.

- Account balance: $25,000
- Risk per trade: 1%
- Entry: 1.0845 (market order, current ask)
- Stop loss: 1.0780 (below the support zone)
- Take profit: 1.0975 (resistance zone, 130-pip target)
- Instrument pip value: $10 per standard lot

**Step 1 — Dollar Risk**:
$25,000 × 0.01 = **$250**

**Step 2 — Stop Loss in Pips**:
(1.0845 – 1.0780) ÷ 0.0001 = 6500 ÷ 1 = **65 pips**

**Step 3 — Lot Size**:
$250 ÷ (65 × $10) = $250 ÷ $650 = **0.38 lots**

You enter 0.38 lots. If stopped out at 1.0780, you lose exactly $247 (rounding from broker's lot step = 0.38). The trade has a 130-pip target, giving a 2:1 reward-to-risk ratio. If you win, you gain $494.

---

## Worked Calculation: XAUUSD Trade (Step by Step)

**Setup**: Short gold trade after a rejection at a key resistance level.

- Account balance: $25,000
- Risk per trade: 0.5% (conservative for gold's volatility)
- Entry: $2,345.00 (short)
- Stop loss: $2,365.00 (above the resistance wicks)
- Take profit: $2,285.00 (260-pip target)
- Instrument pip value: $10 per standard lot

**Step 1 — Dollar Risk**:
$25,000 × 0.005 = **$125**

**Step 2 — Stop Loss in Pips**:
(2,365.00 – 2,345.00) ÷ 0.01 = 20 ÷ 0.01 = **2,000 pips**

Wait — that seems too large. The confusion: brokers often display gold "pips" differently. A move from $2,345.00 to $2,365.00 is a $20 move. At $10/pip per standard lot, and 100 pips = $1, this $20 move = 2,000 pips. Use the price difference directly:

**Alternative approach using price move**: Lot Size = Dollar Risk ÷ (Price Move × $100 per dollar per standard lot):
$125 ÷ ($20.00 × 10) = $125 ÷ $200 = **0.625 lots → round to 0.06 lots**

Or using the calculator format: SL = 20.00 points on gold; at $10/pip per lot, and each $1 move = $100 per lot, and each $0.01 move = $1 per lot: 2,000 pip stop × $10/pip ÷ 100 (scale) = $200 at 1 lot. So: $125 ÷ $200 = 0.625 → broker minimum steps to **0.06 lots**.

**Practical shortcut for gold**: Dollar Risk ÷ (Dollar Price Move × 10) = $125 ÷ ($20 × 10) = 0.625 → **0.06 lots**.

The [TRADE90 gold calculator](/calculator/) handles the gold pip scale conversion automatically.

---

## Why the Formula Alone Isn't Enough

The formula tells you what lot size to enter. It does not tell you:

**When to enter**: Position sizing is neutral on trade quality. A perfectly sized 0.20 lot position on a low-probability setup still has negative expected value. The formula only controls the cost of being wrong — not the frequency of being wrong.

**How to handle partials**: Some traders take partial profits at 1:1 R:R and move their stop to breakeven. If you do this, your actual risk changes mid-trade. Size your initial entry based on the full stop distance, then adjust as the trade progresses.

**Correlated positions**: If you have EUR/USD long and GBP/USD long simultaneously, your effective USD exposure is roughly doubled. Two 1% risk trades on correlated pairs carry closer to 2% aggregate risk. The formula sizes each trade individually — accounting for correlation requires portfolio-level thinking.

**Consistent execution**: The formula must be used on every trade, not just when you remember. Inconsistent application — sizing correctly on planned setups but guessing on impulse trades — is how oversizing errors enter your record.

A position sizing formula combined with a [lot size calculator](/calculator/) and consistent pre-trade discipline produces the mathematical foundation for long-term account growth.

---

## Frequently Asked Questions

**What is the position sizing formula?**
The standard formula is: Lot Size = (Account Balance × Risk %) ÷ (Stop Loss Distance × Pip Value per Standard Lot). This formula adapts to every market by substituting the correct pip value for the instrument being traded.

**How do you calculate lot size?**
Calculate your dollar risk (balance × risk %), determine your stop loss in pips from your entry, then divide dollar risk by (stop pips × pip value per lot). For EUR/USD at $10,000, 1% risk, 50-pip stop: ($10,000 × 0.01) ÷ (50 × $10) = 0.20 lots.

**What is the position sizing formula for futures?**
Futures use the same logic but with contract-specific dollar values. For CME E-mini S&P 500 (ES), each 1-point move = $50 per contract. Lot Size (contracts) = Dollar Risk ÷ (Stop Points × $50). For a $200 risk with a 4-point stop: $200 ÷ (4 × $50) = 1 contract. Always check the specific contract's point value before trading.

**Does the position sizing formula change by market?**
The structure of the formula is identical across all markets — only the pip value changes. USD-quoted forex pairs use $10/pip per standard lot. Gold uses $10/pip per standard lot. NAS100 uses $1/point per lot (most brokers). JPY pairs use ~$6.50–$7.50/pip per standard lot depending on the current USD/JPY rate.

**What is pip value in the formula?**
Pip value is the dollar amount gained or lost when price moves one pip (or one point) in your favor or against you, for one standard lot of the instrument. It is fixed for USD-quoted forex pairs ($10) and gold ($10) but varies for JPY cross pairs based on the current exchange rate. The pip value is the conversion factor between price movement and dollar profit/loss. See the [position sizing guide](/risk-management/position-sizing/) for a full pip value reference table.
