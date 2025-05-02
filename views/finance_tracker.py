import streamlit as st
from components.db import add_expense

def run():
    st.subheader("➕ Add New Expense")
    with st.form("expense_form"):
        amt = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
        cat = st.selectbox("Category", ["Food","Transport","Utilities","Entertainment","Rent","Other"])
        note = st.text_input("Note (optional)")
        if st.form_submit_button("Add Expense"):
            add_expense(amt, cat, note)
            st.success(f"Added ${amt:.2f} to {cat}")
