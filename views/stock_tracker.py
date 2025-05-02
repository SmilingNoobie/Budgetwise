import streamlit as st
import yfinance as yf

def run():
    st.subheader("📈 Stock Price Tracker")
    with st.form("stock_form"):
        sym = st.text_input("Stock Symbol (e.g., AAPL)")
        if st.form_submit_button("Track"):
            stock = yf.Ticker(sym)
            hist = stock.history(period="7d")
            if hist.empty:
                st.error("No data for that symbol.")
            else:
                st.line_chart(hist["Close"])
                st.success(f"Last 7 days of {sym.upper()}")
