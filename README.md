# 📊 Python Financial Planning & Analysis Tool

An automated portfolio tracking and financial reporting tool built with Python.
Fetches **live market data**, computes key performance metrics, and generates
a multi-panel dashboard — simulating a real FP&A reporting workflow.

> **Resume project by:** Srishti Singh
> **GitHub:** github.com/srishtisingh1873228-lgtm/finance-analyzer
---

## 🔍 What This Project Simulates

This project mirrors a core FP&A workflow:

```
Live Data Ingestion → Performance Tracking → Variance Analysis → Visual Reporting
```

| Module | FP&A Equivalent |
|--------|----------------|
| 📋 Watchlist | Real-time price monitoring & daily P&L snapshot |
| 💼 Portfolio Tracker | Holdings valuation & period-over-period return variance |
| 📊 Technical Analysis | Trend identification & momentum-based deviation flagging |
| 🖼 Dashboard | Multi-panel financial report (price, returns, allocation) |
| 📈 Summary Stats | Annualised returns, volatility, and performance KPIs |

---

## 📝 Sample Analysis — AAPL (Nov 2025 – Apr 2026)

> *This is the kind of interpretation an FP&A analyst would write after reviewing the output.*

The 6-month chart shows AAPL trading between **~$240–$285**, with a sharp drawdown in **February 2026**
where price broke below both the 20-day and 50-day moving averages — a bearish crossover signal
indicating a performance deviation from trend.

The RSI (Relative Strength Index) confirmed this, falling near the **oversold threshold (30)**
in early February. Historically, RSI near 30 signals potential reversal — and indeed, price recovered
through March–April, validating the indicator.

Bollinger Bands **widened significantly** during the February drawdown, indicating elevated volatility.
By April, bands narrowed as price stabilized near $265–$270, suggesting consolidation.

Daily returns show the **largest single-day swings clustered in February**, consistent with a period
of market stress — a pattern FP&A teams would flag as an outlier in variance reporting.

**Portfolio concentration risk:** AAPL (36.9%) and MSFT (28.9%) together account for ~66% of total
holdings, making overall portfolio performance heavily correlated to large-cap tech sentiment.

---

## 💼 Portfolio Tracked

| Stock | Shares | Approx. Value |
|-------|--------|--------------|
| AAPL  | 10     | $2,711       |
| MSFT  | 5      | $2,123       |
| GOOGL | 3      | $1,033       |
| AMZN  | 5      | $1,056       |
| NVDA  | 2      | $417         |
| **Total** | — | **~$7,340** |

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python finance_analyzer.py
```

---

## ✏️ Customise It

Edit the top of `finance_analyzer.py`:

```python
PORTFOLIO = {
    "AAPL":  10,   # Change symbols and share counts
    "MSFT":  5,
}

ANALYSIS_TICKER = "AAPL"   # Which stock to analyse deeply
PERIOD          = "6mo"    # 1mo, 3mo, 6mo, 1y, 2y
```

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| `yfinance` | Free Yahoo Finance API — automated data ingestion |
| `pandas` | DataFrames, return calculations, rolling statistics |
| `matplotlib` | Multi-panel dashboard and chart generation |

---

## 📚 Financial Concepts Applied

- **Moving Averages (MA20, MA50)** — trend direction and crossover signals
- **RSI (Relative Strength Index)** — momentum and overbought/oversold detection
- **Bollinger Bands** — volatility measurement and price deviation
- **Daily Return Distribution** — variance analysis and outlier flagging
- **Portfolio Allocation** — concentration risk and diversification review
- **Annualised Volatility** — risk-adjusted performance measurement
