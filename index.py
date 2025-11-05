# api/index.py
import os
import asyncio
import logging
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from crew.crew import run_pipeline

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FinanceCrewAI")

app = FastAPI(title="Finance CrewAI API", version="1.0.1")

# --- Enable CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "🚀 Finance CrewAI API is live!",
        "example": "/api/report?ticker=AAPL&period=1mo"
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/report")
async def report(
    ticker: str = Query("AAPL", description="Ticker symbol, e.g. AAPL or INFY.NS"),
    period: str = Query("1mo", description="Time period (e.g., 1mo, 3mo, 6mo)"),
    format: str = Query("json", description="Output format: json or md"),
):
    try:
        logger.info(f"Running pipeline for {ticker} ({period})")
        # Run pipeline asynchronously
        result = await asyncio.to_thread(run_pipeline, ticker, period)

        safe = jsonable_encoder(result)

        if format == "md":
            return PlainTextResponse(safe.get("report_markdown", "No report."))

        return JSONResponse(content=safe)
    except Exception as e:
        logger.exception("Error running pipeline")
        return JSONResponse(content={"error": str(e)}, status_code=500)
