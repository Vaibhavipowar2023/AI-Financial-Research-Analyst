from typing import List, Dict, Any
import os
import pandas as pd

try:
    import yfinance as yf
    HAS_YFINANCE = True
except Exception:
    HAS_YFINANCE = False

DEFAULT_PERIOD = "1mo"

def fetch_prices(ticker: str, period: str = DEFAULT_PERIOD, interval: str = "1d") -> pd.DataFrame:
    """
    Fetch prices with yfinance when available; else return deterministic synthetic data
    """
    if HAS_YFINANCE:
        t = yf.Ticker(ticker)
        df = t.history(period=period, interval=interval)
        if df.empty:
            raise ValueError(f"No price data for {ticker}.")
        return df
    # fallback deterministic synthetic data (for tests)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
    # deterministic series based on ticker hash for variety
    seed = sum(ord(c) for c in ticker) % 100
    base = 100 + seed
    prices = pd.Series([base + i * 0.5 for i in range(len(dates))], index=dates)
    df = pd.DataFrame({'Close': prices, 'Open': prices - 0.2, 'High': prices + 0.5, 'Low': prices - 0.5, 'Volume': [1000]*len(dates)})
    return df

def fetch_news(ticker: str, limit: int = 6) -> List[Dict[str, Any]]:
    if HAS_YFINANCE:
        t = yf.Ticker(ticker)
        news = t.news or []
        cleaned = []
        for n in news[:limit]:
            cleaned.append({
                "title": n.get("title"),
                "publisher": n.get("publisher"),
                "link": n.get("link"),
                "relatedTickers": n.get("relatedTickers", []),
                "providerPublishTime": n.get("providerPublishTime")
            })
        return cleaned
    # fallback deterministic demo headlines
    return [{"title": f"Demo headline {i+1} about {ticker}", "publisher": "Demo News", "link": "", "relatedTickers": [ticker], "providerPublishTime": None} for i in range(limit)]
