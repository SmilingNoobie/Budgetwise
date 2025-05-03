# views/stock_tracker.py

import streamlit as st
import yfinance as yf
from components.news      import fetch_news
from components.sentiment import aggregate_scores
from components.advisor   import recommend_trade
from components.db        import get_latest_profile

def run():
    st.subheader("📈 Stock Price Tracker")

    # — Existing price chart UI —
    with st.form("stock_form"):
        symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)")
        submitted = st.form_submit_button("Track")
        if submitted and symbol:
            ticker = yf.Ticker(symbol.upper())
            hist = ticker.history(period="7d")
            if hist.empty:
                st.error("No data found for this symbol.")
            else:
                st.line_chart(hist["Close"])
                st.success(f"Showing last 7 days of {symbol.upper()} prices.")

    # — AI Trade Advisor —
    st.markdown("---")
    st.header("🤖 AI Trade Advisor")

    # Ensure we have cash to allocate
    prof = get_latest_profile()
    cash = st.session_state.get("income", 0) + st.session_state.get("savings", 0)
    if cash <= 0:
        st.info(
            "⚠️ Complete your financial profile (Get Started) "
            "so I know how much cash I can allocate."
        )
        return

    symbols = st.text_input("Symbols (comma-separated)", "AAPL,TSLA,AMZN")
    mode    = st.radio("Risk Mode", ["Conservative", "Aggressive"])

    if st.button("Analyze & Recommend"):
        for sym in [s.strip().upper() for s in symbols.split(",")]:
            st.subheader(sym)
            st.write("Fetching news…")
            headlines = fetch_news(sym)

            if not headlines:
                st.warning("No recent news for " + sym)
                continue

            # Compute sentiment over just the headlines
            sentiment = aggregate_scores([h["title"] for h in headlines])
            st.write(f"Sentiment score (–1 to +1): **{sentiment:.2f}**")

            # Get buy/sell recommendation
            rec, units = recommend_trade(
                sym,
                sentiment,
                mode,
                st.session_state.income,
                st.session_state.savings
            )
            st.write(f"**Recommendation:** {rec}")

            # Show the latest headlines as clickable links
            st.markdown("**Latest headlines:**")
            for h in headlines:
                if h.get("source"):
                    st.markdown(f"- [{h['title']}]({h['link']}) — *{h['source']}*")
                else:
                    st.markdown(f"- [{h['title']}]({h['link']})")
