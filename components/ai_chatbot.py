# components/ai_chatbot.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt: str, model: str = "llama3-70b-8192") -> str:
    """Low-level API call to Groq."""
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
    """
        answer any single user question about budgeting.
    """
    prompt = (
        f"User question: {query}\n\n"
        "Give a concise, actionable answer in the context of personal budgeting."
    )
    return call_groq(prompt)

def ask_budgetwise_budget(summary: dict) -> str:
    """
    Given a dict of category->amount, propose a next‐month budget plan + tips.
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

def ask_financial_profile(income: float,
                          goal_1m: float, goal_3m: float,
                          goal_6m: float, goal_1y: float,
                          total_expenses: float,
                          savings: float, debt: float) -> str:
    """
    Generate a personalized AI summary using the full profile:
      - income, goals (1m/3m/6m/1y), expenses, savings, debt
    """
    lines = [
        f"After-tax income: ${income:.2f}",
        f"Total monthly expenses: ${total_expenses:.2f}",
        f"Current savings: ${savings:.2f}",
        f"Current debt: ${debt:.2f}",
        f"1-month investment goal: ${goal_1m:.2f}",
        f"3-month investment goal: ${goal_3m:.2f}",
        f"6-month investment goal: ${goal_6m:.2f}",
        f"1-year investment goal: ${goal_1y:.2f}",
    ]
    prompt = (
        "Here is my complete financial profile:\n"
        + "\n".join(lines)
        + "\n\n"
        "Based on this, provide a comprehensive summary and personalized recommendations: "
        "– identify any red flags; – suggest an optimal monthly budget split; "
        "– propose adjustments to meet my investment goals; – and give 3–5 concrete next steps."
    )
    return call_groq(prompt)
