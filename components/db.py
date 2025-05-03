# components/db.py

import sqlite3
import pandas as pd
import os
from datetime import datetime

# ─── Database file setup ───────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH  = os.path.join(BASE_DIR, "data", "budget.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def connect_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_table():
    conn = connect_db()
    # Expenses table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Financial profiles table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS financial_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            after_tax_income REAL,
            goal_1m REAL,
            goal_3m REAL,
            goal_6m REAL,
            goal_1y REAL,
            total_expenses REAL,
            savings REAL,
            debt REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Trade logs table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS trade_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sentiment REAL,
            recommendation TEXT,
            units REAL,
            mode TEXT  -- 'Conservative' or 'Aggressive'
        )
    """)
    conn.commit()
    conn.close()

# ─── Expense CRUD ──────────────────────────────────────────────────────────────

def add_expense(amount, category, note):
    conn = connect_db()
    conn.execute(
        "INSERT INTO expenses (amount, category, note) VALUES (?, ?, ?)",
        (amount, category, note)
    )
    conn.commit()
    conn.close()

def get_expenses():
    conn = connect_db()
    df = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY created_at DESC",
        conn,
        parse_dates=["created_at"]
    )
    conn.close()
    return df

def update_expense(expense_id: int, amount: float, category: str, note: str):
    conn = connect_db()
    conn.execute(
        "UPDATE expenses SET amount=?, category=?, note=? WHERE id=?",
        (amount, category, note, expense_id)
    )
    conn.commit()
    conn.close()

def delete_expense(expense_id: int):
    conn = connect_db()
    conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def get_summary():
    df = get_expenses()
    if df.empty:
        return 0.0, 0, pd.DataFrame(columns=["category","amount"])

    total = df["amount"].sum()
    count = df.shape[0]
    grouped = (
        df
        .groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )
    return total, count, grouped


# ─── Financial profile CRUD ───────────────────────────────────────────────────

def add_financial_profile(income, g1m, g3m, g6m, g1y, expenses, savings, debt):
    conn = connect_db()
    conn.execute("""
        INSERT INTO financial_profiles
            (after_tax_income, goal_1m, goal_3m, goal_6m, goal_1y,
             total_expenses, savings, debt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (income, g1m, g3m, g6m, g1y, expenses, savings, debt))
    conn.commit()
    conn.close()

def get_latest_profile():
    conn = connect_db()
    df = pd.read_sql_query(
        "SELECT * FROM financial_profiles ORDER BY created_at DESC LIMIT 1",
        conn,
        parse_dates=["created_at"]
    )
    conn.close()
    return df.iloc[0] if not df.empty else None

def update_profile_savings_debt(savings: float, debt: float):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM financial_profiles ORDER BY created_at DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        fid = row[0]
        conn.execute(
            "UPDATE financial_profiles SET savings=?, debt=? WHERE id=?",
            (savings, debt, fid)
        )
        conn.commit()
    conn.close()

# ─── Trade log CRUD ────────────────────────────────────────────────────────────

def log_trade(symbol: str, sentiment: float, recommendation: str, units: float, mode: str):
    conn = connect_db()
    conn.execute("""
        INSERT INTO trade_logs
            (symbol, sentiment, recommendation, units, mode)
        VALUES (?, ?, ?, ?, ?)
    """, (symbol, sentiment, recommendation, units, mode))
    conn.commit()
    conn.close()

def get_trade_logs(limit: int = 100):
    conn = connect_db()
    df = pd.read_sql_query(
        "SELECT * FROM trade_logs ORDER BY timestamp DESC LIMIT ?",
        conn,
        params=(limit,),
        parse_dates=["timestamp"]
    )
    conn.close()
    return df
