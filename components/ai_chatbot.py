import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt: str, model: str = "llama3-70b-8192") -> str:
    if not GROQ_API_KEY:
        return "❌ Groq API key missing. Please set GROQ_API_KEY in your .env"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an AI financial assistant."},
            {"role": "user",   "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.7,
    }

    try:
        r = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Groq API error:", e, getattr(r, "text", ""))
        return "❌ Sorry, I couldn’t reach the AI service."

def ask_budgetwise_ai(query: str) -> str:
    prompt = (
        f"User question: {query}\n\n"
        "Give a concise, actionable answer in the context of personal budgeting."
    )
    return call_groq(prompt)

def ask_budgetwise_budget(summary: dict) -> str:
    """
    summary: dict of category->amount for the current month.
    """
    lines = [f"{cat}: ${amt:.2f}" for cat, amt in summary.items()]
    prompt = (
        "Here is my spending breakdown for this month:\n"
        + "\n".join(lines)
        + "\n\n"
        "Please evaluate my spending and propose a detailed budget plan for next month, "
        "including category targets and 3–5 practical optimization tips."
    )
    return call_groq(prompt)
