"""
========================================
  Finance Analyzer
  Uses: yfinance, pandas, matplotlib
  Run: python finance_analyzer.py
========================================
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────
#  CLI ARGUMENTS (argparse)
# ─────────────────────────────────────────
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Finance Analyzer — Stock Analysis Tool")
    parser.add_argument("--ticker", type=str, default=None,
                        help="Stock ticker to analyse (e.g. AAPL, TSLA, TCS.NS)")
    parser.add_argument("--period", type=str, default=None,
                        help="Time period: 1mo, 3mo, 6mo, 1y, 2y")
    return parser.parse_args()

# ─────────────────────────────────────────
#  SETTINGS — Change these to your liking
# ─────────────────────────────────────────
PORTFOLIO = {
    "AAPL":  10,   # 10 shares of Apple
    "MSFT":  5,    # 5 shares of Microsoft
    "GOOGL": 3,    # 3 shares of Alphabet
    "NVDA":  2,    # 2 shares of NVIDIA
    "AMZN":  4,    # 4 shares of Amazon
}

WATCHLIST = ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "TSLA", "META", "SPY"]

ANALYSIS_TICKER = "AAPL"   # The stock to deep-analyse
PERIOD          = "6mo"    # How far back to look: 1mo, 3mo, 6mo, 1y, 2y

# ─────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────

def color(val, positive="green", negative="red"):
    """Return a coloured string for terminal output."""
    if val > 0:
        return f"\033[92m+{val:.2f}%\033[0m"
    elif val < 0:
        return f"\033[91m{val:.2f}%\033[0m"
    return f"\033[93m{val:.2f}%\033[0m"

def fmt_price(p):
    return f"${p:,.2f}"

def separator(title=""):
    w = 60
    if title:
        side = (w - len(title) - 2) // 2
        print("\n" + "─" * side + f" {title} " + "─" * side)
    else:
        print("\n" + "─" * w)


# ─────────────────────────────────────────
#  MODULE 1 — WATCHLIST PRICES
# ─────────────────────────────────────────

def show_watchlist():
    separator("📋 WATCHLIST")
    print(f"{'Symbol':<8} {'Price':>10} {'1-Day %':>10} {'52W High':>12} {'52W Low':>12}")
    print("─" * 56)
    for sym in WATCHLIST:
        try:
            t    = yf.Ticker(sym)
            info = t.fast_info
            hist = t.history(period="2d")
            if len(hist) < 2:
                continue
            prev  = hist['Close'].iloc[-2]
            cur   = hist['Close'].iloc[-1]
            chg   = ((cur - prev) / prev) * 100
            h52   = info.year_high  if hasattr(info, 'year_high')  else 0
            l52   = info.year_low   if hasattr(info, 'year_low')   else 0
            arrow = "▲" if chg > 0 else "▼" if chg < 0 else "─"
            c     = "\033[92m" if chg > 0 else "\033[91m" if chg < 0 else "\033[93m"
            print(f"{sym:<8} {fmt_price(cur):>10} {c}{arrow}{abs(chg):>7.2f}%\033[0m "
                  f"{fmt_price(h52):>12} {fmt_price(l52):>12}")
        except Exception as e:
            print(f"{sym:<8} {'Error':>10}")


# ─────────────────────────────────────────
#  MODULE 2 — PORTFOLIO TRACKER
# ─────────────────────────────────────────

def show_portfolio():
    separator("💼 PORTFOLIO TRACKER")
    print(f"{'Symbol':<8} {'Shares':>7} {'Price':>10} {'Value':>12} {'Day P&L':>12} {'Day %':>8}")
    print("─" * 62)

    total_value  = 0
    total_daypnl = 0
    rows = []

    for sym, shares in PORTFOLIO.items():
        try:
            hist  = yf.Ticker(sym).history(period="2d")
            if len(hist) < 2:
                continue
            prev  = hist['Close'].iloc[-2]
            cur   = hist['Close'].iloc[-1]
            chg   = ((cur - prev) / prev) * 100
            val   = cur * shares
            daypnl= (cur - prev) * shares
            total_value  += val
            total_daypnl += daypnl
            rows.append((sym, shares, cur, val, daypnl, chg))
        except:
            pass

    for sym, shares, cur, val, daypnl, chg in rows:
        c = "\033[92m" if chg > 0 else "\033[91m" if chg < 0 else "\033[93m"
        sign = "+" if daypnl >= 0 else ""
        print(f"{sym:<8} {shares:>7} {fmt_price(cur):>10} {fmt_price(val):>12} "
              f"{c}{sign}{fmt_price(daypnl):>12}\033[0m {c}{sign}{chg:.2f}%\033[0m")

    print("─" * 62)
    day_pct = (total_daypnl / (total_value - total_daypnl)) * 100 if total_value else 0
    sign = "+" if total_daypnl >= 0 else ""
    c    = "\033[92m" if total_daypnl >= 0 else "\033[91m"
    print(f"{'TOTAL':<8} {'':>7} {'':>10} {fmt_price(total_value):>12} "
          f"{c}{sign}{fmt_price(total_daypnl):>12}\033[0m {c}{sign}{day_pct:.2f}%\033[0m")

    return rows, total_value


# ─────────────────────────────────────────
#  MODULE 3 — TECHNICAL ANALYSIS
# ─────────────────────────────────────────

def compute_indicators(df):
    """Add moving averages, RSI, and Bollinger Bands to a DataFrame."""
    # Moving Averages
    df['MA20']  = df['Close'].rolling(window=20).mean()
    df['MA50']  = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    # RSI (14-period)
    delta = df['Close'].diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Bollinger Bands (20-day, 2 std)
    rolling_mean = df['Close'].rolling(20).mean()
    rolling_std  = df['Close'].rolling(20).std()
    df['BB_Upper'] = rolling_mean + 2 * rolling_std
    df['BB_Lower'] = rolling_mean - 2 * rolling_std

    # Daily returns
    df['Return'] = df['Close'].pct_change() * 100

    return df


def show_technicals(ticker_sym):
    separator(f"📊 TECHNICAL ANALYSIS — {ticker_sym}")
    t    = yf.Ticker(ticker_sym)
    df   = t.history(period=PERIOD)
    df   = compute_indicators(df)

    latest  = df.iloc[-1]
    cur     = latest['Close']
    rsi     = latest['RSI']
    ma20    = latest['MA20']
    ma50    = latest['MA50']

    # RSI signal
    if rsi > 70:
        rsi_signal = "\033[91mOVERBOUGHT (>70) — possible pullback\033[0m"
    elif rsi < 30:
        rsi_signal = "\033[92mOVERSOLD (<30) — possible bounce\033[0m"
    else:
        rsi_signal = "\033[93mNEUTRAL\033[0m"

    # MA signal
    if cur > ma50 > ma20:
        ma_signal = "\033[91mPrice above both MAs — trending up\033[0m"
    elif cur < ma50 and cur < ma20:
        ma_signal = "\033[91mPrice below both MAs — trending down\033[0m"
    else:
        ma_signal = "\033[93mMixed MA signals\033[0m"

    print(f"  Current Price : {fmt_price(cur)}")
    print(f"  20-Day MA     : {fmt_price(ma20)}")
    print(f"  50-Day MA     : {fmt_price(ma50)}")
    print(f"  RSI (14)      : {rsi:.1f}  →  {rsi_signal}")
    print(f"  MA Signal     : {ma_signal}")

    # Volatility
    vol = df['Return'].std()
    print(f"  Volatility    : {vol:.2f}% daily std dev")

    # Best / worst day
    best  = df['Return'].idxmax()
    worst = df['Return'].idxmin()
    print(f"  Best Day      : {best.date()} ({df.loc[best,'Return']:+.2f}%)")
    print(f"  Worst Day     : {worst.date()} ({df.loc[worst,'Return']:+.2f}%)")

    return df


# ─────────────────────────────────────────
#  MODULE 4 — CHARTS
# ─────────────────────────────────────────

def plot_all(df, portfolio_rows, ticker_sym):
    """Generate a 4-panel chart and save as PNG."""
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(16, 12), facecolor="#0d0f14")
    fig.suptitle("Finance Analyzer",
                 fontsize=14, color="#e2e4ee", fontweight="bold", y=0.98)

    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

    ACCENT   = "#00c8db"
    GREEN    = "#4fc842"
    RED      = "#ff5e5e"
    GOLD     = "#f0c030"
    MUTED    = "#8890aa"
    BG_PANEL = "#12151c"
    GRID_C   = "#1e2332"

    def style_ax(ax):
        ax.set_facecolor(BG_PANEL)
        ax.tick_params(colors=MUTED, labelsize=8)
        ax.spines['bottom'].set_color(GRID_C)
        ax.spines['left'].set_color(GRID_C)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.grid(True, color=GRID_C, linewidth=0.5)
        ax.set_axisbelow(True)

    # ── Panel 1: Price + Moving Averages ──────────────
    ax1 = fig.add_subplot(gs[0, :])
    style_ax(ax1)
    ax1.plot(df.index, df['Close'],   color=ACCENT, linewidth=1.8, label='Close', zorder=3)
    ax1.plot(df.index, df['MA20'],    color=GREEN,  linewidth=1.2, linestyle='--', alpha=0.8, label='MA20')
    ax1.plot(df.index, df['MA50'],    color=GOLD,   linewidth=1.2, linestyle='--', alpha=0.8, label='MA50')
    ax1.fill_between(df.index, df['BB_Upper'], df['BB_Lower'], alpha=0.07, color=ACCENT)
    ax1.plot(df.index, df['BB_Upper'], color=ACCENT, linewidth=0.6, alpha=0.4, linestyle=':')
    ax1.plot(df.index, df['BB_Lower'], color=ACCENT, linewidth=0.6, alpha=0.4, linestyle=':')
    ax1.set_title(f"{ticker_sym} Price + Moving Averages + Bollinger Bands ({PERIOD})",
                  color="#e2e4ee", fontsize=10, pad=8)
    ax1.legend(fontsize=8, facecolor=BG_PANEL, labelcolor=MUTED, framealpha=0.7)
    ax1.set_ylabel("Price (USD)", color=MUTED, fontsize=8)

    # ── Panel 2: RSI ──────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])
    style_ax(ax2)
    rsi_colors = [GREEN if r < 30 else RED if r > 70 else ACCENT for r in df['RSI']]
    ax2.plot(df.index, df['RSI'], color=ACCENT, linewidth=1.4)
    ax2.axhline(70, color=RED,   linewidth=0.8, linestyle='--', alpha=0.7)
    ax2.axhline(30, color=GREEN, linewidth=0.8, linestyle='--', alpha=0.7)
    ax2.fill_between(df.index, df['RSI'], 70, where=(df['RSI'] > 70), alpha=0.2, color=RED)
    ax2.fill_between(df.index, df['RSI'], 30, where=(df['RSI'] < 30), alpha=0.2, color=GREEN)
    ax2.set_ylim(0, 100)
    ax2.set_title("RSI (14) — Relative Strength Index", color="#e2e4ee", fontsize=10, pad=8)
    ax2.set_ylabel("RSI", color=MUTED, fontsize=8)
    ax2.text(df.index[2], 72, "Overbought", color=RED,   fontsize=7, alpha=0.8)
    ax2.text(df.index[2], 22, "Oversold",   color=GREEN, fontsize=7, alpha=0.8)

    # ── Panel 3: Daily Returns ────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])
    style_ax(ax3)
    ret_colors = [GREEN if r >= 0 else RED for r in df['Return'].fillna(0)]
    ax3.bar(df.index, df['Return'].fillna(0), color=ret_colors, width=1, alpha=0.85)
    ax3.axhline(0, color=MUTED, linewidth=0.8)
    ax3.set_title("Daily Returns (%)", color="#e2e4ee", fontsize=10, pad=8)
    ax3.set_ylabel("Return %", color=MUTED, fontsize=8)

    # ── Panel 4: Portfolio Pie ────────────────────────
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.set_facecolor(BG_PANEL)
    ax4.spines[:].set_visible(False)
    ax4.tick_params(colors=MUTED)
    if portfolio_rows:
        labels = [r[0] for r in portfolio_rows]
        sizes  = [r[3] for r in portfolio_rows]
        colors = [ACCENT, GREEN, GOLD, "#b880f5", RED, "#ff9842", "#5ba8f5", "#a070e0"]
        wedges, texts, autotexts = ax4.pie(
            sizes, labels=labels, autopct='%1.1f%%',
            colors=colors[:len(labels)], startangle=140,
            wedgeprops=dict(edgecolor=BG_PANEL, linewidth=2),
            textprops=dict(color=MUTED, fontsize=8)
        )
        for at in autotexts:
            at.set_color("#e2e4ee"); at.set_fontsize(8)
    ax4.set_title("Portfolio Allocation", color="#e2e4ee", fontsize=10, pad=8)

    # ── Panel 5: Portfolio Value Bar ──────────────────
    ax5 = fig.add_subplot(gs[2, 1])
    style_ax(ax5)
    if portfolio_rows:
        syms = [r[0] for r in portfolio_rows]
        vals = [r[3] for r in portfolio_rows]
        bar_colors = [GREEN if r[4] >= 0 else RED for r in portfolio_rows]
        bars = ax5.bar(syms, vals, color=bar_colors, alpha=0.85,
                       edgecolor=BG_PANEL, linewidth=1.5)
        for bar, val in zip(bars, vals):
            ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(vals)*0.01,
                     f'${val:,.0f}', ha='center', va='bottom',
                     color=MUTED, fontsize=7)
    ax5.set_title("Portfolio Value by Stock", color="#e2e4ee", fontsize=10, pad=8)
    ax5.set_ylabel("Value (USD)", color=MUTED, fontsize=8)

    plt.savefig("finance_report.pdf", dpi=150, bbox_inches='tight',
                facecolor="#0d0f14", edgecolor='none')
    print("\n  ✅  Chart saved as: finance_report.pdf")
    plt.show()


# ─────────────────────────────────────────
#  MODULE 5 — SUMMARY STATS
# ─────────────────────────────────────────

def show_summary(df, total_value):
    separator("📈 SUMMARY STATS")
    returns = df['Return'].dropna()
    print(f"  Total Portfolio Value : {fmt_price(total_value)}")
    print(f"  {ANALYSIS_TICKER} Avg Daily Return : {returns.mean():.3f}%")
    print(f"  {ANALYSIS_TICKER} Max Daily Gain   : {returns.max():+.2f}%")
    print(f"  {ANALYSIS_TICKER} Max Daily Loss   : {returns.min():+.2f}%")
    print(f"  {ANALYSIS_TICKER} Daily Volatility : {returns.std():.3f}%")
    ann_vol = returns.std() * (252 ** 0.5)
    print(f"  {ANALYSIS_TICKER} Annual Volatility: {ann_vol:.2f}%")
    start = df['Close'].iloc[0]
    end   = df['Close'].iloc[-1]
    total_ret = ((end - start) / start) * 100
    print(f"  {ANALYSIS_TICKER} Period Return    : {total_ret:+.2f}%  ({PERIOD})")


# ─────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────

def main():
    args = parse_args()
    global ANALYSIS_TICKER, PERIOD
    if args.ticker:
        ANALYSIS_TICKER = args.ticker.upper()
    if args.period:
        PERIOD = args.period

    print("\n" + "═" * 60)
    print("   📈  FINANCE ANALYZER")
    print(f"   📅  {datetime.now().strftime('%A, %d %B %Y  %H:%M')}")
    print("═" * 60)
    print("   Fetching live data from Yahoo Finance...\n")

    # 1. Show watchlist
    show_watchlist()

    # 2. Show portfolio
    portfolio_rows, total_value = show_portfolio()

    # 3. Technical analysis
    df = show_technicals(ANALYSIS_TICKER)

    # 4. Summary stats
    show_summary(df, total_value)

    # 5. Generate charts
    separator("🖼  GENERATING CHARTS")
    print("  Building 5-panel chart report...")
    plot_all(df, portfolio_rows, ANALYSIS_TICKER)

    separator()
    print("  Done! Explore the code and change PORTFOLIO / ANALYSIS_TICKER")
    print("  at the top of the file to analyse your own stocks.\n")


if __name__ == "__main__":
    main()
