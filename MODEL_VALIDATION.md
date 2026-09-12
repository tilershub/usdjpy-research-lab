# Model correction and candidate evaluation

## Completed corrections
- RSI returns 100 for uninterrupted gains, 0 for uninterrupted losses and 50 for flat prices.
- Off-calendar macro/driver observations are aligned as-of rather than silently lost when the date is not in the price index.
- Probability validation purges unfinished forward outcomes and samples non-overlapping windows.
- Probability calibration and actual labels now use the same history-derived neutral band.
- Horizon validation chooses its majority direction from training data, not the test outcome distribution; reports coverage and uses non-overlapping forecast windows.
- Unsupported claims that gold spot/futures discrepancies are timing-only are removed.
- A calendar containing only past events is Unknown, not Low risk.
- Price validation rejects future-dated, duplicate, nonfinite and nonpositive history.

These changes can lower previously reported accuracy. Old and new metrics are not directly comparable because the old evaluation had defects and counted overlapping observations.

## Candidate work
`evaluate_candidates.py` compares fixed regularized logistic and shallow random-forest candidates using only causal price features. No revised macro data is used. It trains on the first 60%, selects on the next 20%, then fits on the pre-test observations with a forward-label gap and evaluates the last 20% once. Preprocessing is fitted only on training data. Five-session positions enter at the next close and do not overlap. All predictions, direction, confidence, labels and outcomes are exported.

The report includes all-forecast accuracy and a Wilson interval, training-derived baseline, assumed spread/slippage and financing, net returns, drawdown, and the coverage/accuracy of the >=75% probability subset. Confidence is not accuracy; subset performance cannot stand in for all-forecast performance. The candidate is not automatically promoted to production.

Example:
```
python -m pip install -r requirements-research.txt
python evaluate_candidates.py broker_daily.csv --output research_runs/gold.json --cost-bps 10 --funding-bps 1
```
Input columns: `Date,Close`, chronological unique dates and positive prices. Use a consistent instrument and price basis. Costs in the example are assumptions, not verified broker costs. Obtain sufficient licensed history; the script rejects fewer than 800 usable observations. A 75% validation flag additionally requires >=100 non-overlapping test predictions, the lower 95% accuracy bound >=75%, positive mean net return and outperformance of the test baseline. Even passing that gate needs independent walk-forward/forward testing before any public accuracy claim.

## Current result and blockers
No measured market-data accuracy improvement is claimed. Historical Yahoo downloads were attempted but returned rate limiting/timeouts. Synthetic regression fixtures validate code behavior only, not forecasting skill. Production model weights have not been replaced with an untested candidate.

A licensed historical spot gold/CFD dataset is still needed to replace gold futures research. Calendar coverage requires a working authorized data feed. Existing FRED history is not vintage/release-time data; production historical macro tests remain limited and are explicitly marked as such. Broker bid/ask, slippage, funding calendars and intraday stop execution are not modeled by the close-to-close candidate. No 75%+ result has been established.

Sources: https://scikit-learn.org/stable/common_pitfalls.html and https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
