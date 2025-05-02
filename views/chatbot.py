import streamlit as st
from components.ai_chatbot import ask_budgetwise_ai

def run():
    st.subheader("🤖 Ask BudgetWise AI")

    user_input = st.text_area(
        "What would you like help with? (e.g., “How can I save on groceries?”)",
        height=150
    )

    if st.button("Ask AI"):
        if not user_input.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking…"):
                answer = ask_budgetwise_ai(user_input)
            st.success("Here’s what I found:")
            st.write(answer)
