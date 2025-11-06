import streamlit as st
from dotenv import load_dotenv
from crew.crew import run_pipeline
import datetime as dt

# --- Load environment variables ---
load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="Finance CrewAI – Market Summary",
    layout="centered",
)

st.title("Finance CrewAI – Market Summary Assistant")

st.markdown("""
Type a company name or stock ticker (e.g., *Infosys*, *AAPL*, *TSLA*, *RELIANCE.NS*)  
and click **Generate Report** to get a detailed news and market summary.
""")

# --- Cache pipeline execution ---
@st.cache_data(ttl=3600, show_spinner=False)
def cached_run_pipeline(ticker: str):
    """Cache the run_pipeline call to avoid repeated API hits."""
    return run_pipeline(ticker=ticker, period="1mo")

# --- Ticker Map ---
TICKER_MAP = {
    "infosys": "INFY.NS",
    "apple": "AAPL",
    "tesla": "TSLA",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "hdfc": "HDFCBANK.NS",
}

def main():
    query = st.text_input("Enter company name or ticker symbol:", placeholder="e.g. Infosys or AAPL").strip()

    if st.button("Generate Report"):
        if not query:
            st.warning("Please enter a company or ticker name.")
            return

        q = query.lower()
        ticker = TICKER_MAP.get(q, query.upper())

        st.markdown(f"### Selected Ticker: `{ticker}`")

        with st.spinner(f"Generating market report for {ticker}..."):
            try:
                result = cached_run_pipeline(ticker)
            except Exception as e:
                st.error(f"Could not generate report.\n\n**Error:** {e}")
                return

        if not result:
            st.error("No data returned from the pipeline.")
            return

        st.success("Report generated successfully!")

        px = result.get("price_snapshot") or {}
        st.divider()
        st.subheader("Price Snapshot")
        col1, col2, col3 = st.columns(3)
        col1.metric("Last Close", px.get("last_close", "N/A"))
        col2.metric("First Close", px.get("first_close", "N/A"))
        col3.metric("Change (%)", px.get("change_pct", "N/A"))

        st.divider()
        st.subheader("Full Market Report")
        st.markdown(result.get("report_markdown", "_No report available._"))

        sentiment = result.get("sentiment", "")
        if isinstance(sentiment, dict):
            sentiment = sentiment.get("overall", "")
        if sentiment:
            st.markdown(f"### Sentiment Overview: **{sentiment}**")

        st.divider()
        news_summary = result.get("news_summary", "")
        if not news_summary.strip():
            st.info("No recent news found for this company.")
        else:
            with st.expander("News Summary", expanded=True):
                st.markdown(news_summary)

        report_text = result.get("report_markdown", "")
        if report_text:
            st.download_button(
                label="Download Report",
                data=report_text,
                file_name=f"{ticker}_market_report_{dt.date.today()}.md",
                mime="text/markdown",
            )

        st.divider()

if __name__ == "__main__":
    main()
