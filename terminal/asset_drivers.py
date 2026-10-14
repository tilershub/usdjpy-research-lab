"""Instrument-specific macro research checklist.

Watch drivers do NOT assert that an input is currently moving the market.
A value becomes evidence only when joined with a timestamped, licensed source
and an observed reaction window. Facts, hypotheses and unknowns stay separate.
"""
from copy import deepcopy

CATALOG = {
 "XAU/USD": {
  "name": "Spot Gold (XAU/USD)", "asset": "precious_metal",
  "focus": "Gold is non-yielding, globally priced in USD; safe-haven demand can conflict with real-yield pressure.",
  "drivers": [
   ("US real yields and Fed path", "Higher real yields may increase the opportunity cost of holding non-yielding gold.", "US TIPS yields, Fed futures, FOMC commentary", "daily / event"),
   ("USD and risk regime", "USD strength can pressure USD-denominated gold, but dollar and gold can both rise under risk-off.", "Broad trade-weighted USD, USD pairs, equity volatility", "intraday"),
   ("Inflation and oil shock", "Supply-driven oil inflation may change policy-rate expectations, real yields and demand for hedges.", "WTI/Brent, official CPI/PCE releases, yield response", "event / intraday"),
   ("Central-bank and physical demand", "Reserve accumulation, jewelry demand and ETF flows affect structural demand.", "World Gold Council, central-bank disclosures, physically backed ETF flows", "monthly / daily"),
   ("Institutional futures positioning", "Crowding and leverage can amplify reversals; CFTC is delayed, not a live order book.", "CFTC COMEX gold COT, futures open interest", "weekly"),
   ("Geopolitical and fiscal uncertainty", "War, sanctions, tariffs or debt policy can raise hedging demand or also raise the USD/yields.", "Primary government announcements + independent contemporaneous reporting", "event"),
  ],
  "risk": "COMEX futures, XAU/USD spot and each broker's CFD are distinct price bases; confirm spread and contract specification.",
 },
 "EUR/USD": {
  "name": "EUR/USD", "asset": "spot_fx",
  "focus": "Relative Fed-versus-ECB policy, US-Eurozone growth, capital flows and broad USD risk are primary context.",
  "drivers": [
   ("Fed versus ECB expectations", "Relative forward policy rates matter more than a single central-bank decision.", "Fed/ECB statements, front-end OIS curves", "daily / event"),
   ("Relative inflation and labor data", "Surprises versus consensus can change the expected rate differential.", "BLS CPI/NFP; Eurostat HICP; consensus timestamp", "event"),
   ("US versus Eurozone yields", "Changes in two-year yield spreads can lead short-term FX repricing.", "US/Germany 2-year government yields", "intraday / daily"),
   ("Energy import exposure", "Higher oil/gas costs can worsen euro-area terms of trade depending on policy reaction.", "TTF gas, Brent, import/export reports", "daily / event"),
   ("Trade and fiscal policy", "Tariffs and fiscal decisions can alter growth outlook and flows.", "Official EU/US policy documents, primary announcements", "event"),
   ("Positioning and funding", "EUR futures flows and FX options skew can signal risk concentration, not live order depth.", "CFTC EUR FX futures, options risk reversals", "weekly / daily"),
  ],
  "risk": "There is no consolidated spot FX order book; 'liquidity' zones inferred from price are proxies only.",
 },
 "GBP/USD": {
  "name": "GBP/USD", "asset": "spot_fx",
  "focus": "BoE-Fed repricing, UK inflation/wages, gilt yields and UK fiscal credibility.",
  "drivers": [
   ("BoE versus Fed", "Rate differentials change sterling carry and direction.", "BoE MPC, FOMC, Sonia/SOFR OIS", "daily / event"),
   ("UK wages and inflation", "Sticky services inflation and wages can surprise policy expectations.", "ONS CPI, UK payroll/earnings releases", "event"),
   ("Gilts and fiscal decisions", "UK fiscal credibility or supply concerns can add a sterling risk premium.", "HM Treasury, DMO, UK gilt curves", "event / daily"),
   ("USD strength and global risk", "Broad dollar shocks can dominate local UK positives.", "USD index, US front-end yields, volatility", "intraday"),
   ("Positioning", "Leveraged GBP futures positions may affect squeeze risk.", "CFTC GBP COT; options skew", "weekly / daily"),
  ],
  "risk": "Sterling can fall even on stronger UK inflation if gilt risk/fiscal confidence dominates.",
 },
 "USD/JPY": {
  "name": "USD/JPY", "asset": "spot_fx",
  "focus": "US-Japan rate differentials, yen funding/carry, BoJ policy and intervention risk.",
  "drivers": [
   ("US versus Japan yield spread", "Short- and long-term nominal yields can drive carry incentives.", "US/Japan government yields and swap curves", "intraday / daily"),
   ("BoJ and Fed policy paths", "Policy guidance and inflation reprice differentials.", "BoJ/FRB releases; Japan CPI/wages; US CPI/NFP", "event"),
   ("MOF intervention", "Official yen intervention warnings or operations can overwhelm technical levels.", "Japan Ministry of Finance and BoJ announcements", "event"),
   ("Global risk and carry unwinding", "Risk-off can strengthen yen when funded carry positions unwind; not guaranteed.", "Equity volatility, cross-yen pairs, FX options", "intraday"),
   ("Energy imports", "Higher imported energy costs can worsen Japan's terms of trade.", "Crude oil, import bill/trade balances", "daily / monthly"),
   ("JPY positioning", "Leveraged futures shorts may amplify squeezes.", "CFTC JPY futures positioning", "weekly"),
  ],
  "risk": "FX intervention and policy comments can produce gaps; broker spot/CFD spreads widen in volatile periods.",
 },
 "USD/CHF": {
  "name": "USD/CHF", "asset": "spot_fx",
  "focus": "SNB-Fed differentials, CHF safe-haven demand and Swiss inflation.",
  "drivers": [
   ("SNB versus Fed", "Relative rate path affects USD/CHF yield differential.", "SNB policy releases, FOMC, yield spreads", "event / daily"),
   ("Safe-haven flows", "CHF may strengthen during geopolitical stress even if USD is strong.", "CHF crosses, risk measures, Swiss flows", "intraday"),
   ("SNB FX operations", "SNB reserves and communications matter for CHF supply.", "SNB disclosures, balance sheet and statements", "monthly / event"),
   ("Inflation and exports", "Swiss inflation and export demand may influence policy.", "Swiss FSO CPI, SECO and trade data", "monthly"),
  ],
  "risk": "The SNB can alter policy unexpectedly and safe-haven narratives compete with USD strength.",
 },
 "USD/CAD": {
  "name": "USD/CAD", "asset": "spot_fx",
  "focus": "Fed-BoC rates, Canadian growth and crude oil terms of trade.",
  "drivers": [
   ("Fed versus BoC", "Rate expectations affect USD/CAD and carry.", "Fed/BoC statements, US/Canadian yield spreads", "event / daily"),
   ("WTI and Canadian terms of trade", "Oil shifts can influence CAD but are not a mechanical inverse USD/CAD rule.", "WTI, Western Canadian Select, exports", "intraday / daily"),
   ("US and Canada labor/inflation", "Surprises drive relative policy repricing.", "BLS; Statistics Canada CPI/labor", "event"),
   ("Trade policy", "Tariff or USMCA changes can affect cross-border outlook.", "US/Canadian government announcements", "event"),
   ("Risk and funding", "Broad USD strength may dominate an oil rally.", "DXY, Treasury yields, global volatility", "intraday"),
  ],
  "risk": "Oil exposure depends on grades, export flows and global USD effects; avoid one-factor CAD stories.",
 },
 "AUD/USD": {
  "name": "AUD/USD", "asset": "spot_fx",
  "focus": "RBA-Fed differential, China activity, metals, risk appetite and commodity demand.",
  "drivers": [
   ("RBA versus Fed", "Relative policy and Australian wages/CPI drive carry.", "RBA/RBA minutes, ABS CPI, SOFR/RBA rates", "event / daily"),
   ("China activity", "China demand affects Australia's export commodity outlook.", "China PMI/industrial production/credit data", "event / monthly"),
   ("Iron ore and commodities", "Metals and bulk commodity prices can alter terms of trade.", "Iron ore index, copper and trade data", "daily"),
   ("Global risk and USD", "AUD often trades as cyclical/risk-sensitive currency, with frequent exceptions.", "USD, equities, credit spreads, VIX", "intraday"),
   ("Positioning", "AUD futures crowding may amplify macro reactions.", "CFTC AUD COT", "weekly"),
  ],
  "risk": "China-policy headlines and metals may lead AUD in different directions from US rates.",
 },
 "NZD/USD": {
  "name": "NZD/USD", "asset": "spot_fx",
  "focus": "RBNZ-Fed, New Zealand domestic cycle, China demand and global risk.",
  "drivers": [
   ("RBNZ versus Fed", "Relative policy yields influence NZD carry.", "RBNZ releases, FOMC, NZ-US rates", "event / daily"),
   ("NZ inflation and employment", "Small open economy and policy sensitivity.", "Stats NZ CPI/employment, RBNZ forecasts", "event"),
   ("China/Asia demand", "Exports exposed to Asian growth changes.", "China PMI and New Zealand trade data", "monthly / event"),
   ("Dairy auction and commodity returns", "Milk product prices may alter export income expectations.", "Global Dairy Trade auction, export prices", "biweekly / monthly"),
   ("Global risk", "USD funding/risk-off often matters to cyclical NZD.", "Dollar, global credit, equity volatility", "intraday"),
  ],
  "risk": "Dairy/China signals must be contextualized against policy spreads and global dollar regime.",
 },
 "BTC/USD": {
  "name": "BTC/USD spot", "asset": "crypto",
  "focus": "Spot demand, liquidations, leverage, liquidity conditions and regulatory flows.",
  "drivers": [
   ("Dollar liquidity and rates", "Tighter liquidity and higher real yields may pressure risk assets; correlations vary.", "USD, US yields, credit conditions", "intraday / daily"),
   ("Spot ETF net flows", "Exchange-traded investment flows can support or weaken spot demand.", "Fund sponsor filings and verified creations/redemptions", "daily"),
   ("Derivatives leverage", "Liquidations, funding and open interest can amplify volatility.", "Exchange futures OI, funding, liquidations", "intraday"),
   ("On-chain flows", "Movements to/from exchanges may suggest potential selling or custody changes, not intent.", "Timestamped validated on-chain data", "hourly / daily"),
   ("Regulation, tariffs and geopolitics", "News can alter access, sentiment and volatility.", "SEC/CFTC notices, legislation, primary statements", "event"),
   ("Market structure and exchange basis", "Venue prices and liquidity can diverge; perpetuals differ from spot.", "Selected exchange bid/ask, spread, venue volumes", "intraday"),
  ],
  "risk": "No consolidated Bitcoin price or CFD market; show venue and instrument basis with timestamps.",
 },
}


def research_driver_profile(symbol):
    item = CATALOG.get(symbol)
    if item is None:
        return None
    return {
        "instrument": symbol,
        "focus": item["focus"],
        "driver_watchlist": [
            {
                "driver": driver,
                "transmission": why,
                "required_evidence": evidence,
                "cadence": cadence,
                "status": "not_assessed",
            } for driver, why, evidence, cadence in item["drivers"]
        ],
        "market_structure_limit": item["risk"],
        "interpretation_rule": (
            "Potential driver only. Do not claim market causality without verified "
            "event time, actual/expected data and timestamp-aligned asset reaction."
        ),
    }
