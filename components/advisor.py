# components/advisor.py

from components.db import log_trade

def recommend_trade(symbol: str,
                    sentiment: float,
                    mode: str,
                    income: float,
                    savings: float) -> tuple[str, float]:
    """
    Given sentiment [-1,1], mode ('Conservative'/'Aggressive'),
    income & savings, return (recommendation_text, units).
    """
    # Compute disposable cash
    cash = max(income + savings, 0)
    # Base fraction to allocate
    if mode == "Conservative":
        alloc_pct = 0.05  # 5% of cash
    else:
        alloc_pct = 0.15  # 15% of cash

    if sentiment > 0.1:
        # buy
        usd = cash * alloc_pct * sentiment
        units = usd / fetch_price(symbol)
        rec = f"Buy ~{units:.2f} shares ({usd:.2f}$ at sentiment {sentiment:.2f})"
    elif sentiment < -0.1:
        # sell
        units = cash * alloc_pct * (-sentiment) / fetch_price(symbol)
        rec = f"Sell ~{units:.2f} shares"
    else:
        units = 0.0
        rec = "Hold, sentiment neutral"
    # Log it
    log_trade(symbol, sentiment, rec, units, mode)
    return rec, units

def fetch_price(symbol: str) -> float:
    # lightweight: use yfinance here
    import yfinance as yf
    ticker = yf.Ticker(symbol)
    price = ticker.history(period="1d")["Close"][-1]
    return float(price)
