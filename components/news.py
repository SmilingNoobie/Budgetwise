# components/news.py

import feedparser
from urllib.parse import quote

symbol_map = {
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "AMZN": "Amazon",
    "META": "Meta",
    "GOOG": "Google",
    "SPY": "S&P 500",
    "NASDAQ": "Nasdaq",
    "WALMART": "Walmart",
    "TQQQ": "ProShares TQQQ",
    "NVDA": "NVIDIA"
}

def fetch_news(symbol: str) -> list[dict]:
    """
    Returns up to 5 recent headlines for symbol from Google News RSS,
    each as {title, link, source}.
    """
    query = quote(f"{symbol_map.get(symbol, symbol)} stock when:1d")
    url   = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed  = feedparser.parse(url)
    out   = []
    for entry in feed.entries[:5]:
        title  = entry.title
        link   = entry.link
        # feedparser sometimes puts the source in entry.source.title
        source = entry.get("source", {}).get("title", "")
        out.append({"title": title, "link": link, "source": source})
    return out
