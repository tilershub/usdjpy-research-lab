from django.shortcuts import render

from .models import ContentPage


FEATURED_SOURCE_PATHS = [
    "articles/psychology/why-traders-fail.md",
    "articles/risk-management/risk-of-ruin.md",
    "articles/trading-plans/how-to-build-a-trading-plan.md",
    "articles/prop-firms/prop-firm-rules-explained.md",
    "articles/performance/trading-journal-guide.md",
    "articles/psychology/revenge-trading.md",
]


def home(request):
    pages = {page.source_path: page for page in ContentPage.objects.filter(source_path__in=FEATURED_SOURCE_PATHS).live()}
    featured = [pages[path] for path in FEATURED_SOURCE_PATHS if path in pages]
    return render(request, "website/home.html", {"featured": featured})


CALCULATORS = {
    "position": ("Position Size Calculator", "Calculate a risk-controlled lot size from balance, risk and stop distance."),
    "drawdown": ("Drawdown Calculator", "Measure compound drawdown after a losing streak and the gain required to recover."),
    "risk_reward": ("Risk / Reward Calculator", "Check reward-to-risk, break-even win rate and expectancy before a trade."),
    "pip_value": ("Pip Value Calculator", "Calculate approximate pip value for a USD-denominated trading account."),
    "profit": ("Profit / Loss Calculator", "Estimate a trade result from instrument, lot size and price movement."),
    "compounding": ("Compounding Calculator", "Project account growth from a consistent monthly return."),
}


def calculator(request, tool):
    title, description = CALCULATORS[tool]
    return render(request, "website/calculator.html", {"tool": tool, "title": title, "description": description})


def today(request):
    checklist = {
        "Pre-Session": ["Checked the economic calendar for high-impact news", "Marked key levels on my instruments", "Confirmed risk per trade and daily budget", "Reviewed my trading-plan setups", "I am rested and not trading to recover yesterday"],
        "In Session": ["Position sized every trade before entry", "Respected my maximum trade count", "No entries after my daily risk budget was spent"],
        "Post-Session": ["Logged every trade in the journal", "Graded plan adherence honestly", "Closed the platform — no revenge session"],
    }
    return render(request, "website/today.html", {"title": "Today — Daily Trading Dashboard", "description": "Market sessions, daily risk budget, checklist and journal snapshot.", "checklist": checklist})


def journal(request):
    stats = [("Trades", "j-s-trades"), ("Win Rate", "j-s-winrate"), ("Expectancy", "j-s-expectancy"), ("Profit Factor", "j-s-pf"), ("Net R", "j-s-netr"), ("Adherence", "j-s-adherence")]
    return render(request, "website/journal.html", {"title": "Trading Journal — Track Trades & Expectancy", "description": "Private browser-based trading journal with R-multiple statistics and plan adherence.", "stats": stats})


def trading_plan(request):
    sections = [
        ("markets", "01", "Markets & Instruments", "Which instruments will you trade — and only these?"),
        ("sessions", "02", "Sessions & Schedule", "When are you at the screen and which windows do you trade?"),
        ("setups", "03", "Setup Definition", "Define entry criteria another trader could execute."),
        ("risk", "04", "Risk Parameters", "Risk per trade, daily cap, trade count and drawdown response."),
        ("management", "05", "Trade Management", "Stops, targets, partials and break-even rules."),
        ("review", "06", "Review Process", "Journaling cadence and weekly/monthly reviews."),
    ]
    return render(request, "website/trading_plan.html", {"title": "Trading Plan Builder", "description": "Build, save and export a six-section trading plan.", "sections": sections})
