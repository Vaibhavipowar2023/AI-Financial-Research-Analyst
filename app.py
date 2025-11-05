import streamlit as st
from dotenv import load_dotenv
from crew.crew import run_pipeline
import datetime as dt

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Finance CrewAI – Market Summary",
    page_icon="📊",
    layout="centered",
)

st.title("📊 Finance CrewAI – Market Summary Assistant")

st.markdown("""
Type a company name or stock ticker (e.g., *Infosys*, *AAPL*, *TSLA*, *RELIANCE.NS*)  
and click **Generate Report** to get a detailed news and market summary.
""")

# User input
query = st.text_input("Enter company name or ticker symbol:", placeholder="e.g. Infosys or AAPL")

# Button
if st.button("Generate Report"):
    if not query.strip():
        st.warning("Please enter a company or ticker name.")
        st.stop()

    # --- Step 1: Detect basic ticker ---
    q = query.lower()
    ticker_map = {
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
    ticker = ticker_map.get(q, query.upper())

    st.markdown(f"### 🏢 Selected Ticker: `{ticker}`")

    # --- Step 2: Run Crew pipeline ---
    with st.spinner(f"Generating market report for {ticker}..."):
        try:
            result = run_pipeline(ticker=ticker, period="1mo")
        except Exception as e:
            st.error(f"Error while running analysis: {e}")
            st.stop()

    # --- Step 3: Display Results ---
    st.success("✅ Report generated successfully!")

    # Price snapshot
    px = result.get("price_snapshot", {})
    st.markdown(f"""
    **📈 Price Snapshot**
    - Last Close: `{px.get('last_close', 'N/A')}`
    - First Close: `{px.get('first_close', 'N/A')}`
    - Change (%): `{px.get('change_pct', 'N/A')}`
    """)

    # Full markdown report
    st.markdown("---")
    st.markdown("### 🧠 Full Market Report")
    st.markdown(result.get("report_markdown", "_No report available._"))

    # # --- Optional: Display sub-sections separately ---
    with st.expander("📰 News Summary"):
        st.markdown(result.get("news_summary", "_No news summary available._"))

    # with st.expander("📊 Indicators Summary"):
    #     st.markdown(result.get("indicators_summary", "_No indicator summary available._"))
    #
    # with st.expander("🎯 Strategy"):
    #     st.markdown(result.get("strategy", "_No strategy available._"))

    # # --- Optional: Download report ---
    # report_text = result.get("report_markdown", "")
    # if report_text:
    #     st.download_button(
    #         label="📥 Download Report",
    #         data=report_text,
    #         file_name=f"{ticker}_market_report_{dt.date.today()}.md",
    #         mime="text/markdown",
    #     )
