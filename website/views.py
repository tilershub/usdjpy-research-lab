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
