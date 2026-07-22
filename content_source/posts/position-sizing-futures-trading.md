---
title: "Position Sizing for Futures Trading Explained — Contracts, Ticks, and Risk"
excerpt: "Futures sizing uses contracts and tick values instead of lots and pips. The risk math is identical once you know the instrument. Here's the complete guide with worked examples for every major futures market."
published_at: "2026-05-14"
updated_at: "2026-05-14"
tags:
  - "Futures"
  - "Position Sizing"
  - "Contracts"
  - "Day Trading"
  - "NinjaTrader"
primary_tag: "Futures"
meta_title: "Position Sizing for Futures Trading — Contracts, Tick Values, and Risk | TRADE90"
meta_description: "How to size futures positions using tick values and contract counts. Complete formula, tick value table for ES, NQ, CL, GC, and worked examples. Free position size calculator."
reading_time: 10
author: "TRADE90"
---

Futures traders think in contracts. Forex traders think in lots. The vocabulary differs; the underlying risk math is the same formula. Once you know your instrument's tick value, calculating the right number of contracts takes 30 seconds.

---

## Futures Sizing vs Forex Sizing

| Forex | Futures |
|---|---|
| Position size unit: **lots** | Position size unit: **contracts** |
| Price movement unit: **pips** | Price movement unit: **ticks** |
| Risk calculation: Stop pips × pip value × lots | Risk calculation: Stop ticks × tick value × contracts |
| Fractional positions (0.01 lots) | Whole contracts only (use micros for precision) |
| Leverage applied per lot | Leverage embedded in contract multiplier |

The formula is structurally identical. The only adjustment is replacing "pip value" with "tick value" and expressing stop distance in ticks instead of pips.

---

## The Futures Position Sizing Formula

```
Dollar Risk  = Account Balance × (Risk % ÷ 100)
Stop in $    = Stop Ticks × Tick Value per Contract
Contracts    = Dollar Risk ÷ Stop in $
```

Round down. You cannot hold fractional contracts. When the result is below 1, use micro contracts.

---

## Complete Tick Value Reference

| Symbol | Name | Exchange | Tick Size | Tick Value | Daily Range (typical) |
|---|---|---|---|---|---|
| ES | E-mini S&P 500 | CME | 0.25 pts | $12.50 | 40–80 pts |
| NQ | E-mini Nasdaq 100 | CME | 0.25 pts | $5.00 | 150–300 pts |
| YM | E-mini Dow Jones | CBOT | 1 pt | $5.00 | 200–400 pts |
| RTY | E-mini Russell 2000 | CME | 0.10 pts | $5.00 | 30–60 pts |
| MES | Micro E-mini S&P | CME | 0.25 pts | $1.25 | — (10% of ES) |
| MNQ | Micro E-mini Nasdaq | CME | 0.25 pts | $0.50 | — (10% of NQ) |
| CL | Crude Oil | NYMEX | $0.01/bbl | $10.00 | $1–$3 |
| GC | Gold | COMEX | $0.10/oz | $10.00 | $20–$50 |
| SI | Silver | COMEX | $0.005/oz | $25.00 | $0.30–$0.80 |
| ZB | 30-Year T-Bond | CBOT | 1/32 pt | $31.25 | 1–3 pts |
| NG | Natural Gas | NYMEX | $0.001 | $10.00 | $0.10–$0.30 |
| 6E | Euro FX | CME | 0.00005 | $6.25 | 0.005–0.015 |
| 6J | Japanese Yen | CME | 0.0000005 | $6.25 | 0.003–0.008 |

---

## Worked Example 1: ES (S&P 500 E-mini)

**Setup**: Long ES on H1 breakout  
**Account**: $75,000 | **Risk**: 0.5% = $375  
**Entry**: 5,200.00 | **Stop**: 5,196.00 (4-point stop = 16 ticks)

```
Stop in $  = 16 ticks × $12.50 = $200
Contracts  = $375 ÷ $200 = 1.875 → 1 contract
```

At 1 ES contract: risk = $200 (0.27% of $75,000 — below target but the next contract would be $400/0.53%)

**Precision solution**: 1 ES + 1 MES
- 1 ES: $200 risk
- 1 MES: $200 ÷ 10 = $20 risk (but $20 additional doesn't close the gap)

Better: 3 MES extra = 3 × $20 = $60. Total: $200 + $60 = $260 (0.35%). Closest achievable to target.

---

## Worked Example 2: NQ (Nasdaq E-mini)

**Setup**: Short NQ on H4 resistance  
**Account**: $100,000 | **Risk**: 0.5% = $500  
**Entry**: 19,500 | **Stop**: 19,560 (60-point stop = 240 ticks)

```
Stop in $  = 240 ticks × $5.00 = $1,200
Contracts  = $500 ÷ $1,200 = 0.42 → 0 full contracts
```

0 NQ contracts — the stop is too wide for 0.5% at this account size. Solution: MNQ

```
Stop in $ (MNQ) = 240 ticks × $0.50 = $120
Contracts (MNQ) = $500 ÷ $120 = 4.17 → 4 MNQ contracts
```

4 MNQ = 0.4 NQ equivalent. Risk = 4 × $120 = $480 (0.48% — very close to target).

---

## Worked Example 3: CL (Crude Oil)

**Setup**: Long CL on supply breakout  
**Account**: $40,000 | **Risk**: 1% = $400  
**Entry**: $72.00 | **Stop**: $71.60 ($0.40 below entry = 40 ticks)

```
Stop in $ = 40 ticks × $10.00 = $400
Contracts = $400 ÷ $400 = 1 contract
```

Exactly 1 CL contract at exactly 1% risk. CL has no micro equivalent — if your stop is $0.60 ($600 risk per contract), skip or tighten the structural stop if possible.

---

## Worked Example 4: GC (Gold Futures)

**Setup**: Gold long on daily structure  
**Account**: $50,000 | **Risk**: 0.5% = $250  
**Entry**: $2,310 | **Stop**: $2,280 ($30 below entry = 300 ticks)

```
Stop in $ = 300 ticks × $10.00 = $3,000
Contracts = $250 ÷ $3,000 = 0.08 → 0 contracts
```

Gold futures ($30 move = $3,000 risk per contract) require large accounts for 0.5% risk with structure-based stops. At $50,000 with 0.5% risk, only a 2.5-point ($250/300 ticks, $833 stop) stop would allow 1 contract. Use the XAUUSD CFD instead for smaller accounts — the calculator at [/calculator/xauusd/](/calculator/xauusd/) covers CFD gold sizing.

---

## Account Size Requirements by Contract Type

At 1% risk per trade, with typical intraday stop distances:

| Contract | Typical Stop | Risk/Contract | Min Account (1%) | Min Account (0.5%) |
|---|---|---|---|---|
| ES | 4 pts (16 ticks) | $200 | $20,000 | $40,000 |
| NQ | 15 pts (60 ticks) | $300 | $30,000 | $60,000 |
| YM | 60 pts (60 ticks) | $300 | $30,000 | $60,000 |
| MES | 4 pts (16 ticks) | $20 | $2,000 | $4,000 |
| MNQ | 15 pts (60 ticks) | $30 | $3,000 | $6,000 |
| CL | $0.30 (30 ticks) | $300 | $30,000 | $60,000 |

---

## Scaling from Micro to Full Contracts

The professional progression for futures traders:

| Phase | Account Size | Sizing Approach |
|---|---|---|
| Learning | $5,000–$15,000 | Micro contracts only (MES, MNQ) |
| Developing | $15,000–$40,000 | Mix of micro and full |
| Established | $40,000–$100,000 | Full contracts primary |
| Professional | $100,000+ | Multiple full contracts |

Move from micro to full when a single full contract represents 0.5–1% of your account at your typical stop distance. Until then, micro contracts provide the precision you need.

---

## Frequently Asked Questions

**How do I calculate futures position size?**
Contracts = (Account Balance × Risk %) ÷ (Stop Ticks × Tick Value). Round down. Use micro contracts if the result is less than 1.

**What is a tick in futures trading?**
The minimum price increment for a futures contract. Each tick has a fixed dollar value (tick value) that is exchange-defined. ES ticks are worth $12.50. NQ ticks are worth $5.00.

**How many ES contracts should I trade with $50,000?**
At 0.5% risk ($250) with a 4-point stop (16 ticks × $12.50 = $200): 1 contract. At 1% risk ($500): 2 contracts.

**Is futures position sizing different from forex?**
The formula structure is identical. The units differ: lots vs contracts, pips vs ticks, pip value vs tick value. Once you know the tick value, the same three-step formula applies.

**What is the minimum account for ES day trading?**
One ES contract at a 4-point stop risks $200. For 1% risk, you need $20,000. For 0.5% risk (recommended for funded traders): $40,000. Use MES for accounts below these thresholds.
