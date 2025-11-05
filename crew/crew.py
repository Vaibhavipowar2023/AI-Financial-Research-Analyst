import logging
from typing import Dict, Any

from crew.agents.factory import build_agents
from crew.tasks import (
    make_news_task,
    make_indicators_task,
    make_strategy_task,
    make_report_task,
)
from utils.market import fetch_prices, fetch_news
from services.indicators import sma, ema, rsi
from crew.core.crewai_shim import Crew

logger = logging.getLogger(__name__)


def price_snapshot(prices) -> Dict[str, Any]:
    """Generate a price snapshot summary."""
    if prices is None or "Close" not in prices.columns:
        return {"last_close": None, "first_close": None, "change_pct": None}

    last_close = float(prices["Close"].iloc[-1])
    first_close = float(prices["Close"].iloc[0])
    change_pct = (last_close - first_close) / first_close * 100.0
    return {
        "last_close": round(last_close, 2),
        "first_close": round(first_close, 2),
        "change_pct": round(change_pct, 2),
    }


def run_pipeline(ticker: str = "AAPL", period: str = "1mo") -> Dict[str, Any]:
    """
    Full Crew pipeline: Fetch prices & news, compute indicators, summarize results,
    and generate a professional markdown market report.
    """
    logger.info(f"Running Crew pipeline for {ticker} ({period})")

    # 1️⃣ Fetch price data & news
    prices = fetch_prices(ticker=ticker, period=period)
    news = fetch_news(ticker=ticker, limit=6)
    px_snap = price_snapshot(prices)

    # 2️⃣ Compute indicators
    try:
        rsi_val = round(rsi(prices["Close"]).iloc[-1], 2)
        ema_val = round(ema(prices["Close"], 14).iloc[-1], 2)
        sma_val = round(sma(prices["Close"], 50).iloc[-1], 2)
        ind_summary = f"RSI(14): {rsi_val}, EMA(14): {ema_val}, SMA(50): {sma_val}"
    except Exception as e:
        logger.warning(f"Indicator calculation failed: {e}")
        ind_summary = "Indicators not available."

    # 3️⃣ Prepare context
    headlines = "\n".join(
        [f"- {n.get('title','No title')} ({n.get('publisher','Unknown')})" for n in news]
    ) or "No recent news available."

    context = {
        "ticker": ticker,
        "price_snapshot": px_snap,
        "snapshot": ind_summary,
        "headlines": headlines,
    }

    # 4️⃣ Build agents
    agents = build_agents()

    # --- NEWS ---
    t_news = make_news_task(agents["news"], context)
    news_out = Crew([agents["news"]], [t_news]).kickoff()
    news_summary = getattr(news_out, "raw", str(news_out))

    # --- INDICATORS ---
    t_ind = make_indicators_task(agents["finance"], context)
    ind_out = Crew([agents["finance"]], [t_ind]).kickoff()
    indicators_summary = getattr(ind_out, "raw", str(ind_out))

    # --- STRATEGY ---
    context["news_summary"] = news_summary
    context["indicators_summary"] = indicators_summary
    t_strategy = make_strategy_task(agents["strategy"], context)
    strat_out = Crew([agents["strategy"]], [t_strategy]).kickoff()
    strategy_text = getattr(strat_out, "raw", str(strat_out))

    # --- REPORT ---
    report_context = {
        **context,
        "strategy": strategy_text,
    }
    t_report = make_report_task(agents["report"], report_context)
    report_out = Crew([agents["report"]], [t_report]).kickoff()
    report_md = getattr(report_out, "raw", str(report_out))

    # --- CLEAN OUTPUTS ---
    def clean(text):
        if not isinstance(text, str):
            return ""
        return text.replace("<s>", "").replace("</s>", "").strip()

    return {
        "ticker": ticker,
        "period": period,
        "price_snapshot": px_snap,
        "indicators_summary": clean(indicators_summary),
        "news_summary": clean(news_summary),
        "strategy": clean(strategy_text),
        "report_markdown": clean(report_md),
    }
