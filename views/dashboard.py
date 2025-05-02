import streamlit as st
from components.db import get_summary
from components.ai_chatbot import ask_budgetwise_budget
import yfinance as yf
import plotly.express as px

def run():
    st.subheader("📊 Budget Dashboard Overview")

    # 1) Expenses summary
    total, monthly, count, grouped = get_summary()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Expenses", f"${total:.2f}")
    c2.metric("This Month", f"${monthly:.2f}")
    c3.metric("Records Logged", count)

    # 2) Bar chart (dark theme)
    st.markdown("### Spending by Category")
    bar = px.bar(
        grouped, x="category", y="amount",
        labels={"amount": "Amount ($)", "category": "Category"},
        title="Expenses This Month",
        template="plotly_dark",
        color="amount",
        color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(bar, use_container_width=True)

    # 3) AI Budget Suggestions button (moved below chart)
    if st.button("How am I doing this month?"):
        summary = dict(zip(grouped["category"], grouped["amount"]))
        with st.spinner("Analyzing your spending…"):
            advice = ask_budgetwise_budget(summary)
        st.subheader("💡 AI-Generated Budget Plan & Tips")
        st.write(advice)

    # 4) Stock Watchlist
    st.markdown("### 📈 Your Stock Watchlist")
    symbols = st.text_input("Enter stock symbols (comma-separated)", "AAPL, TSLA")
    period = st.selectbox("Select historical period", ["1d","7d","1mo","6mo","ytd","5y"], index=1)

    if st.button("Update Watchlist"):
        syms = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        for sym in syms:
            st.markdown(f"#### {sym}")
            try:
                ticker = yf.Ticker(sym)
                hist = ticker.history(period=period)
                if hist.empty:
                    st.error(f"No data for {sym}")
                else:
                    fig = px.line(
                        hist, x=hist.index, y="Close",
                        title=f"{sym} Price ({period})",
                        template="plotly_dark",
                        labels={"index":"Date","Close":"Close Price ($)"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error fetching {sym}: {e}")
