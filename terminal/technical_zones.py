"""Technical price-zone candidates derived exclusively from closed OHLC bars.

Zones represent observed price reactions, NOT resting orders, dealer liquidity,
stop locations or predictions. No entry/stop-loss advice is generated.
"""
from datetime import datetime


def _candidate(index, kind, candle):
    level = candle["high"] if kind == "high" else candle["low"]
    return {"value": level, "index": index, "kind": kind,
            "observed_at": candle["open_at"].isoformat()}


def _confirmed_pivots(candles, left=2, right=2):
    # Latest right bars are needed for a CONFIRMED pivot. This explicitly avoids
    # the common retrospective-lookahead problem in swing-indicator charts.
    pivots = []
    for i in range(left, len(candles) - right):
        curr = candles[i]
        window = candles[i-left:i+right+1]
        high = curr["high"]
        low = curr["low"]
        if all(high >= c["high"] for c in window) and any(high > c["high"] for c in window):
            pivots.append(_candidate(i, "high", curr))
        if all(low <= c["low"] for c in window) and any(low < c["low"] for c in window):
            pivots.append(_candidate(i, "low", curr))
    return pivots


def _cluster(points, tolerance):
    """Greedy level clustering, separately for swing highs and lows."""
    groups = []
    for point in sorted(points, key=lambda p: p["value"]):
        target = next((g for g in groups if abs(g["center"] - point["value"]) <= tolerance), None)
        if target is None:
            groups.append({"center": point["value"], "members": [point]})
        else:
            target["members"].append(point)
            target["center"] = sum(v["value"] for v in target["members"]) / len(target["members"])
    return groups


def technical_zones(candles, atr, *, lookback=100):
    """Identify nearest observable reactions around LAST completed close.

    Requires 55+ validated closed candles. Uses confirmed 2/2 pivots, keeps
    potential zones strictly above or below the latest close, and reports a
    broker-independent invalidation *question* rather than an execution stop.
    """
    if len(candles) < 55 or atr <= 0:
        return {
            "status": "unavailable",
            "detail": "Insufficient completed OHLC data or measurable range for price zones.",
            "overhead": [], "underfoot": [],
        }
    recent = candles[-min(lookback, len(candles)):]
    latest = recent[-1]["close"]
    tolerance = max(atr * .25, latest * .00003)
    pivots = _confirmed_pivots(recent)
    result = {"overhead": [], "underfoot": []}
    for kind, key in (("high", "overhead"), ("low", "underfoot")):
        points = [p for p in pivots if p["kind"] == kind]
        groups = _cluster(points, tolerance)
        for group in groups:
            members = group["members"]
            lowest = min(m["value"] for m in members)
            highest = max(m["value"] for m in members)
            # Allow a finite ATR-scaled band around exact swing price.
            center = group["center"]
            floor = min(lowest, center - tolerance / 2)
            ceiling = max(highest, center + tolerance / 2)
            if key == "overhead" and floor <= latest:
                continue
            if key == "underfoot" and ceiling >= latest:
                continue
            last = max(members, key=lambda m: m["index"])
            result[key].append({
                "zone_low": round(floor, 6),
                "zone_high": round(ceiling, 6),
                "center": round(center, 6),
                "distance_pct": round(abs(center / latest - 1) * 100, 3),
                "distance_atr": round(abs(center - latest) / atr, 2),
                "confirmed_swing_count": len(members),
                "last_observed_at": last["observed_at"],
                "classification": ("Potential overhead swing-high resistance" if kind == "high"
                                   else "Potential swing-low support"),
                "stop_cluster_proxy": len(members) >= 2,
                "interpretation": (
                    "Repeated swing highs might attract stop orders above them; order flow is NOT verified."
                    if kind == "high" and len(members) >= 2 else
                    "Repeated swing lows might attract stop orders below them; order flow is NOT verified."
                    if kind == "low" and len(members) >= 2 else
                    "A prior completed swing, not proof of active supply or demand."
                ),
            })
        result[key].sort(key=lambda z: z["distance_atr"])
        result[key] = result[key][:3]
    # These are factual range extremes measured from *prior* completed bars,
    # not hidden dealer-book orders or guaranteed support and resistance.
    prior = recent[-21:-1]
    return {
        "status": "derived_from_closed_candles",
        "reference_close": round(latest, 6),
        "atr_reference": round(atr, 6),
        "overhead": result["overhead"],
        "underfoot": result["underfoot"],
        "previous20_high": round(max(c["high"] for c in prior), 6),
        "previous20_low": round(min(c["low"] for c in prior), 6),
        "method": "2-bar confirmed swing pivots clustered within 0.25 ATR; max 100 closed bars.",
        "limitations": [
            "Zones are historical price-reaction proxies; CFD liquidity and resting orders are not observable.",
            "No level can prevent a stop loss being triggered. Spread, slippage, news gaps and your broker's contract matter.",
            "A level is not an entry signal. Confirmation or invalidation requires future observations.",
        ],
    }
