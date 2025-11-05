import os
import logging
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# --- Config ---
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://openrouter.ai/api/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct:free")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)


def llm(prompt: str, retries: int = 2) -> str:
    """
    General-purpose LLM call used by main Crew agents.
    Includes retry logic for stability.
    """
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "https://financecrewai.local",
                    "X-Title": "Finance CrewAI",
                },
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"[Attempt {attempt+1}] LLM error: {e}")
            time.sleep(1)
    return "LLM_REMOTE_ERROR: Unable to retrieve response."


def llm_concise(prompt: str, retries: int = 2) -> str:
    """
    Short-response variant used for summarization or headlines.
    """
    concise_prompt = f"Summarize concisely:\n\n{prompt}\n\nReturn in 1-2 sentences only."
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": concise_prompt}],
                extra_headers={
                    "HTTP-Referer": "https://financecrewai.local",
                    "X-Title": "Finance CrewAI",
                },
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"[Attempt {attempt+1}] LLM concise error: {e}")
            time.sleep(1)
    return "LLM_REMOTE_ERROR: Unable to retrieve concise response."
