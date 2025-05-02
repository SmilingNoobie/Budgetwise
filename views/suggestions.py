import streamlit as st
from components.utils import get_budget_tips

def run():
    st.subheader("💡 Budget Suggestions")
    for tip in get_budget_tips():
        st.info(tip)
