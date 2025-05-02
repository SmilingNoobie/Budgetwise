import sqlite3
import pandas as pd
import os
from datetime import datetime

DB_FILE = "data/budget.db"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def connect_db():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def create_table():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

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
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY created_at DESC", conn)
    conn.close()
    return df

def get_summary():
    df = get_expenses()
    if df.empty:
        return 0, 0, 0, pd.DataFrame()
    df["created_at"] = pd.to_datetime(df["created_at"])
    total = df["amount"].sum()
    grouped = df.groupby("category")["amount"].sum().reset_index()
    now = datetime.now()
    monthly = df[df["created_at"] >= pd.Timestamp(now.replace(day=1))]["amount"].sum()
    return total, monthly, df.shape[0], grouped
