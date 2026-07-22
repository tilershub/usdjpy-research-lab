---
title: "7 Position Sizing Mistakes That Fail Funded Accounts — And How to Fix Each One"
excerpt: "Most funded account failures aren't strategy failures — they're math failures. These 7 position sizing mistakes account for the majority of blown prop firm evaluations and funded accounts. Identify which ones apply to your trading before your next challenge."
published_at: "2026-04-10"
updated_at: "2026-04-10"
tags:
  - "Position Sizing"
  - "Funded Trading"
  - "Risk Management"
  - "Prop Firm"
  - "FTMO"
  - "Trading Mistakes"
primary_tag: "Risk Management"
meta_title: "7 Position Sizing Mistakes That Fail Funded Accounts | TRADE90"
meta_description: "The 7 most common position sizing mistakes that blow prop firm challenges and funded accounts. Includes the exact math showing why each mistake fails — and how to fix it."
reading_time: 9
author: "TRADE90"
---

You can have a genuinely profitable strategy — positive expectancy, clean entry triggers, disciplined exits — and still blow a funded account. The mechanism is almost always the same: position sizing that amplifies normal losing streaks into account-ending drawdown events.

Here are the 7 mistakes that appear repeatedly in blown funded accounts. Most traders make at least 3 of them without realizing it.

---

## Mistake 1: Using a Fixed Lot Size Instead of a Risk Percentage

**What it looks like**: "I always trade 0.10 lots on EUR/USD."

**Why it fails**: A fixed lot size means your risk per trade changes with every different stop loss. At 0.10 lots with a 30-pip stop, you risk $30. The same 0.10 lots with a 90-pip stop risks $90 — three times as much from the same position size.

On funded accounts, this creates a situation where structurally wider stops (which are often the correct stops) cause you to unknowingly take 2–3× your intended risk. A sequence of setups requiring wider stops can push your total risk exposure to 10–15% of account in a single session.

**The fix**: Always calculate risk as a percentage of your current account balance, not as a fixed lot size. The formula is:

```
Lot Size = (Account Balance × Risk %) ÷ (Stop Loss Pips × Pip Value)
```

Use the [TRADE90 position size calculator](/) to run this calculation automatically. The 2 seconds it takes is the most valuable 2 seconds in your trading session.

---

## Mistake 2: Not Accounting for Spread in Your Risk Calculation

**What it looks like**: Setting a 50-pip stop loss but not factoring in a 3-pip spread on the entry.

**Why it fails**: On a 0.10 lot position with a 3-pip spread and a 50-pip stop, your actual total cost at stop-out is 53 pips × $1.00 = $53, not $50. That's a 6% underestimate of your true risk. On instruments like GBP/JPY or exotic pairs with 8–15 pip spreads, the underestimate is far larger.

During volatile market conditions (news events, low-liquidity sessions), spreads can widen to 3–5× their normal levels. A trade entered during the London open with a widening spread can immediately put you 10–15 pips offside before price even starts moving against you.

**The fix**: Add your broker's typical spread to the stop loss distance in your position size calculation. If you're targeting a 50-pip stop on GBP/USD with a 2-pip spread, use 52 pips in the calculation. Use a slightly wider stop on instruments with variable spreads.

---

## Mistake 3: Scaling Into Losing Positions

**What it looks like**: "I'll average down — if it was a good entry at $2,310, it's even better at $2,290."

**Why it fails**: This is the single most dangerous position sizing behavior on funded accounts, and it's responsible for more blown evaluations than any other single mistake.

When you add to a losing position:
- Your total position size grows
- Your average entry price shifts (improves slightly)
- But your total dollar risk grows faster than your average entry improves

A trader who enters 0.05 lots of XAUUSD at $2,310 with a $2,280 stop ($300 risk) and then adds another 0.05 lots at $2,295 has now doubled their position. If price reaches $2,280, they lose:
- First entry: 30 pips × $10 × 0.05 lots = $15 (loss on first position)
- Second entry: 15 pips × $10 × 0.05 lots = $7.50 (loss on second position)

Wait — that doesn't seem so bad. But if they move the stop to accommodate the new entry — say to $2,270 — the math changes:
- First entry at $2,310: 40 pip loss × $10 × 0.05 lots = $20
- Second entry at $2,295: 25 pip loss × $10 × 0.05 lots = $12.50
- Total loss: $32.50

That's 65% more risk than the original trade planned for, taken on a trade that is already moving against them. This is how small setbacks become account-ending events.

**The fix**: The only acceptable scaling is into winning positions (pyramiding). Never add to a losing trade. If the original setup was valid, trust the original stop. If the stop is hit, exit. Re-evaluate from clean.

---

## Mistake 4: Misunderstanding Correlated Instruments

**What it looks like**: Taking three separate trades — EUR/USD long, GBP/USD long, and EUR/GBP long — thinking they represent three independent 0.5% risks.

**Why it fails**: EUR/USD and GBP/USD move together roughly 85% of the time during normal conditions. EUR/GBP is mathematically derived from EUR/USD and GBP/USD. Opening all three simultaneously is not three independent positions — it is approximately 1.5× a single directional bet on USD weakness.

If USD strengthens unexpectedly (a surprise CPI print, for example), all three positions reverse simultaneously. Three 0.5% losses = 1.5% daily drawdown — not the 0.5% you thought you were risking.

**The fix**: Count correlated positions against the same risk pool, not separately. If you have two highly correlated positions open simultaneously, treat them as a single position for daily risk calculation purposes. The TRADE90 daily risk tracker shows total daily exposure so you can see combined risk across all open positions.

---

## Mistake 5: Not Reducing Size After Drawdown

**What it looks like**: Maintaining 1% risk per trade after losing 5% of the account.

**Why it fails**: Consider a $100,000 funded account that has drawn down to $95,000. The trader continues risking 1% per trade ($950 per trade, calculated on the current balance). This is technically within the rules — but the account is now $5,000 from breach, with the maximum drawdown limit at $90,000.

At $950 risk per trade, just 5 more losing trades = $4,750 additional loss = account at $90,250 — one trade away from the 10% max drawdown limit.

**The fix**: When drawdown exceeds 3–4%, reduce position size. A common professional approach is to scale down to 0.25% risk per trade once drawdown reaches 4%, and to 0.10% at 6% drawdown. The math compounds in your favor: smaller size during drawdown means the losses slow, giving your edge time to recover.

---

## Mistake 6: Leaving Positions Open Through High-Impact News

**What it looks like**: A trade is open during Non-Farm Payrolls. The stop is 50 pips away. "I'll just hold through — the stop will handle it."

**Why it fails**: High-impact news events (NFP, FOMC, CPI, central bank rate decisions) can move markets 100–300+ pips in under 30 seconds. During this period, slippage makes your stop loss non-functional — the broker cannot fill your stop at the stated price because the bid/ask is moving faster than the order book can process.

A 50-pip stop that you expect to limit your loss to $500 on a standard lot can actually result in a $1,500–$2,000 loss due to slippage on a major news event. On a funded account, this single event can breach your daily loss limit in one candle.

**The fix**: Close positions 5 minutes before any high-impact news event (red-flag events on the economic calendar). After the initial volatility subsides (typically 5–10 minutes post-release), re-evaluate the new structure and re-enter if the setup is still valid.

---

## Mistake 7: Using the "Martingale" Recovery Approach

**What it looks like**: "I lost $100 on that trade. I'll risk $200 on the next one to get it back fast."

**Why it fails**: Doubling position size after a loss is the fastest known path to blowing a funded account. The mathematics:

| Consecutive Loss # | Trade Size (2x each) | Cumulative Loss |
|---|---|---|
| Loss 1 | 1% | 1% |
| Loss 2 | 2% | 3% |
| Loss 3 | 4% | 7% |
| Loss 4 | 8% | 15% |

By the fourth consecutive loss — which is not unusual in any trading strategy — you have lost 15% of your account. That's beyond FTMO's 10% maximum drawdown. The evaluation is over before you reach the fifth trade.

A losing streak of 4 trades at increasing sizes is something that happens to every trader. With fixed 0.5% risk, 4 consecutive losses = 2% drawdown — a speed bump, not a crisis.

**The fix**: Keep position size fixed as a percentage of account balance. Never increase size to "recover" a loss. If you feel the urge to double size after a loss, step away from the platform for 30 minutes minimum.

---

## The Common Thread: Emotional Override of a Mathematical System

Every mistake on this list has an emotional component. Averaging down feels like smart cost-basis management. Adding size after a loss feels like taking back control. Holding through news feels like conviction in the trade.

These impulses exist in every trader. The difference between traders who pass funded evaluations and those who don't is not the absence of these impulses — it is the presence of a system that makes acting on them structurally impossible.

That system is the **Trade90 Safety System**:
1. 0.5% maximum risk per trade — enforced by calculator, not willpower
2. 1% maximum daily risk — logged in the daily tracker, not estimated mentally
3. No scaling into losers — the position size is set once before entry and does not change

Use the [TRADE90 position sizer](/) before every single trade. Run the numbers. Write the lot size down. Then execute. The 2 seconds this takes is the only thing standing between you and the 90%+ failure rate that most funded traders experience.

---

## Position Sizing Self-Audit

Before your next trading session, answer these questions honestly:

1. Do you calculate your exact lot size using a formula before every trade? _(Yes/No)_
2. Is your risk per trade always expressed as a percentage, never a fixed lot size? _(Yes/No)_
3. Have you ever added to a losing position in the last 30 days? _(Yes/No)_
4. Do you account for spread when calculating your stop loss risk? _(Yes/No)_
5. Do you know your exact total risk exposure (across all open positions) at every point in the trading day? _(Yes/No)_
6. Do you close positions before red-flag news events? _(Yes/No)_
7. Have you ever doubled position size after a losing trade? _(Yes/No)_

Any "No" on questions 1, 2, 4, 5, or 6 — or any "Yes" on questions 3 or 7 — represents a concrete risk management failure that, left uncorrected, will eventually terminate a funded account.

Fix the failures before the next trade. Not before the next challenge. Now.

---

## Tools Referenced in This Article

- [Position Size Calculator](/) — run every trade through this before entry
- [Funded Trader Risk Calculator](/funded-trader-risk-calculator/) — Trade90 Safety System with daily tracker
- [How to Calculate Position Size](/how-to-calculate-position-size/) — complete formula guide with worked examples
- [Prop Firm Risk Management Framework](/prop-firm-risk-management/) — the full Trade90 risk discipline system
