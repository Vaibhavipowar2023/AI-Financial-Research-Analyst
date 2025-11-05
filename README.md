
#  AI Financial Research Analyst – CrewAI-Powered Market Intelligence System

> 🚀 An AI-powered financial research assistant that analyzes stock prices, market news, and technical indicators to produce **insightful, data-driven trading recommendations** — powered by **CrewAI**, **FastAPI**, **Streamlit**, and **Mistral-7B-Instruct (OpenRouter)**.

---

## 🧠 Overview

**AI Financial Research Analyst** simulates the workflow of a professional market analyst.
It fetches live market data, financial news, computes key indicators (RSI, SMA, EMA), and leverages an **LLM** to generate human-like insights and trading suggestions.

The project supports both:

* 🖥️ **Streamlit Dashboard** — for interactive exploration
* ⚙️ **FastAPI REST API** — for backend or integrations

---

## 🧩 Key Features

✅ Real-time stock price and % change
✅ AI-generated financial news summaries
✅ Technical indicators (RSI, EMA, SMA)
✅ Sentiment & strategy recommendation (Buy / Hold / Sell)
✅ Markdown report generation with emojis
✅ Deployed-ready architecture for **Vercel (FastAPI)** or **Streamlit Cloud**

---

## 💻 Tech Stack

| Layer         | Technology                              |
| ------------- | --------------------------------------- |
| Frontend      | Streamlit                               |
| Backend       | FastAPI                                 |
| AI Model      | 🧠 **Mistral-7B-Instruct (OpenRouter)** |
| Data Source   | Yahoo Finance                           |
| Language      | Python 3.10+                            |
| Deployment    | Vercel (API) + Streamlit Cloud / Local  |
| Orchestration | CrewAI-style modular agents             |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Vaibhavipowar2023/AI-Financial-Research-Analyst.git
cd AI-Financial-Research-Analyst
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\activate     # Windows
source .venv/bin/activate    # macOS / Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` File

```
OPENROUTER_API_KEY=sk-or-your-valid-key
BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=mistralai/mistral-7b-instruct:free
DEFAULT_TICKER=AAPL
DEFAULT_PERIOD=1mo
```

> ⚠️ Never commit `.env` — it’s already ignored via `.gitignore`.

---

## 🧭 Usage

### 🟢 Run Streamlit App

```bash
streamlit run app.py
```

Visit → [http://localhost:8501](http://localhost:8501)

---

### ⚙️ Run FastAPI Server

```bash
uvicorn index:app --reload
```

Then visit:

* JSON: [http://127.0.0.1:8000/api/report?ticker=AAPL&period=1mo](http://127.0.0.1:8000/api/report?ticker=AAPL&period=1mo)
* Markdown: [http://127.0.0.1:8000/api/report?ticker=AAPL&period=1mo&format=md](http://127.0.0.1:8000/api/report?ticker=AAPL&period=1mo&format=md)

---

## 🧾 Example Output

### **JSON Response**

```json
{
  "ticker": "INFY.NS",
  "period": "1mo",
  "price_snapshot": {
    "last_close": 1467.9,
    "first_close": 1453.74,
    "change_pct": 0.97
  },
  "news_summary": "Infosys beats Q2 estimates, expands AI partnerships.",
  "strategy": "BUY - Positive sentiment and strong fundamentals.",
  "report_markdown": "📊 Infosys Market Summary ..."
}
```

### **Markdown Summary (LLM Output)**

> 📊 **Infosys Market Summary (Nov 2025)**
>
> * Current Price: ₹1,467.9 (+0.97%)
> * RSI: 42 (neutral)
> * Sentiment: Positive
> * Recommendation: ✅ **BUY** for short-term swing
```

📁 Project Structure

finance_research_analyst/
│
├── api/ or index.py          # FastAPI entrypoint
├── app.py                    # Streamlit app (frontend)
├── config/                   # YAML config files
├── crew/                     # CrewAI pipeline & agents
├── services/                 # LLM + indicators services
├── utils/                    # Market + news utils
├── requirements.txt
├── vercel.json
└── .env (ignored)



```
---
🧠 AI Model Details

| Parameter  | Value                                                        |
| ---------- | ------------------------------------------------------------ |
| Model      | **Mistral-7B-Instruct (free)**                               |
| Provider   | OpenRouter                                                   |
| API URL    | [https://openrouter.ai/api/v1](https://openrouter.ai/api/v1) |
| Purpose    | Generate natural-language summaries and trade insights       |
| Advantages | Fast, low-latency, balanced factual accuracy                 |



🧱 CrewAI Agents

| Agent        | Function                            |
| ------------ | ----------------------------------- |
| **news**     | Summarizes market headlines         |
| **finance**  | Analyzes indicators (RSI, EMA, SMA) |
| **strategy** | Suggests Buy / Hold / Sell decision |
| **report**   | Compiles final markdown report      |

---
```
## 🧠 Future Enhancements

* 🪄 Portfolio analysis across multiple tickers
* 🧾 10-K / 10-Q financial statement summarization
* 🧩 Vector memory for company-specific context
* 🎙️ Voice-based financial assistant
* 📊 Advanced visualization with Plotly



