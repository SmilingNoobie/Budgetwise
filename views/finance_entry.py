# views/add_expense.py

import streamlit as st
from components.db import (
    add_expense, get_expenses, update_expense,
    delete_expense, get_latest_profile, update_profile_savings_debt
)

def run():
    st.header("Add & Manage Your Finances")

    # ─── 1) Add New Expense ───────────────────────────────────────────────────────
    st.subheader("➕ Add New Expense")
    with st.form("add_exp_form"):
        amt  = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
        cat  = st.selectbox("Category",
            ["Food","Transport","Utilities","Entertainment","Rent","Other"]
        )
        note = st.text_input("Note (optional)")
        if st.form_submit_button("Add Expense"):
            add_expense(amt, cat, note)
            st.success(f"Added ${amt:.2f} to {cat}")
    st.markdown("---")

    # ─── 2) Edit / Delete Existing Expenses ─────────────────────────────────────
    st.subheader("📝 Edit or Delete Expenses")
    df = get_expenses()
    if df.empty:
        st.info("No expenses logged yet.")
    else:
        st.dataframe(df[["id","amount","category","note","created_at"]], width=700)
        selected_id = st.selectbox("Expense ID to Edit", df["id"].tolist())
        exp = df[df["id"] == selected_id].iloc[0]
        with st.form("edit_form"):
            new_amt  = st.number_input(
                "Amount ($)",
                value=float(exp["amount"]),
                format="%.2f"
            )
            new_cat  = st.selectbox(
                "Category",
                ["Food","Transport","Utilities","Entertainment","Rent","Other"],
                index=["Food","Transport","Utilities","Entertainment","Rent","Other"]
                    .index(exp["category"])
            )
            new_note = st.text_input("Note", value=exp["note"] or "")
            if st.form_submit_button("Save Changes"):
                update_expense(selected_id, new_amt, new_cat, new_note)
                st.success("Expense updated.")
        if st.button("Delete Expense"):
            delete_expense(selected_id)
            st.success("Expense deleted.")
    st.markdown("---")

    # ─── 3) Update Savings & Debt ────────────────────────────────────────────────
    st.subheader("💾 Update Savings & Debt")
    prof = get_latest_profile()
    if prof is not None:
        with st.form("profile_form"):
            sav  = st.number_input(
                "Savings ($)",
                value=float(prof["savings"]),
                format="%.2f"
            )
            debt = st.number_input(
                "Debt   ($)",
                value=float(prof["debt"]),
                format="%.2f"
            )
            if st.form_submit_button("Save Profile"):
                update_profile_savings_debt(sav, debt)
                st.success("Profile updated.")
    else:
        st.info("Please complete Get Started first.")
