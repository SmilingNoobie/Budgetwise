# 💼 BudgetWise – Personal Finance & AI Tracker

**BudgetWise** is an all-in-one personal finance app built with Streamlit.  
Track your expenses, set savings goals, monitor investments, and get AI-powered financial insights.

## 🚀 Features
- 💸 Add and categorize expenses
- 📊 Dashboard with bar charts & Sankey flow
- 🎯 Set 1M–1Y financial goals
- 🤖 AI chatbot for budgeting advice
- 📈 Stock sentiment tracker

## 🛠 Tech Stack
- Python + Streamlit
- SQLite for local data
- Plotly for charts

## 🔧 Setup
1. Clone the repo  
2. Install dependencies:
pip install -r requirements.txt
3. Run the app:
streamlit run app.py

## 📦 Folder Structure
📁 components/ # Database + helpers
📁 views/ # Pages: dashboard, entry, chatbot, etc.
📁 data/ # SQLite DB (auto-created)
app.py # Main entry
