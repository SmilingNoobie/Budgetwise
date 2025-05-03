# views/get_started.py

import streamlit as st
import pandas as pd
import plotly.express as px
from components.db import add_financial_profile
from components.ai_chatbot import ask_financial_profile

def go_to_dashboard():
    """Switch back to Dashboard."""
    st.session_state.selection = "Dashboard"

def run():
    st.title("Let’s Get Started with Your Financial Plan")
    st.image("static/robot.png", width=180)  # only on this page

    # ─── Initialize session state ───────────────────────────────────────────────
    for key, default in [
        ("step", 0),
        ("income", 0.0),
        ("g1m", 0.0),
        ("g3m", 0.0),
        ("g6m", 0.0),
        ("g1y", 0.0),
        ("expenses_list", []),
        ("savings", 0.0),
        ("debt", 0.0),
        ("ai_advice", "")
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ─── Step Navigation ─────────────────────────────────────────────────────────
    def next_step():
        st.session_state.step += 1
    def prev_step():
        if st.session_state.step > 0:
            st.session_state.step -= 1

    steps = [
        "Enter your monthly after‑tax income",
        "Set your investment goals",
        "Add your monthly expenses",
        "Input savings & debt",
        "Review & get AI summary"
    ]
    st.markdown(f"### Step {st.session_state.step + 1}: {steps[st.session_state.step]}")

    # ─── Step 1: Income ───────────────────────────────────────────────────────────
    if st.session_state.step == 0:
        st.session_state.income = st.number_input(
            "Monthly After‑Tax Income ($)",
            min_value=0.0,
            format="%.2f",
            value=st.session_state.income
        )

    # ─── Step 2: Goals ────────────────────────────────────────────────────────────
    elif st.session_state.step == 1:
        st.session_state.g1m = st.slider(
            "1‑Month Investment Goal ($)",
            0.0, 1000.0, st.session_state.g1m, step=50.0
        )
        st.session_state.g3m = st.slider(
            "3‑Month Investment Goal ($)",
            0.0, 5000.0, st.session_state.g3m, step=100.0
        )
        st.session_state.g6m = st.slider(
            "6‑Month Investment Goal ($)",
            0.0, 10000.0, st.session_state.g6m, step=250.0
        )
        st.session_state.g1y = st.slider(
            "1‑Year Investment Goal ($)",
            0.0, 100000.0, st.session_state.g1y, step=1000.0
        )

    # ─── Step 3: Dynamic Expenses ─────────────────────────────────────────────────
    elif st.session_state.step == 2:
        st.markdown("#### Add an expense to your list")
        with st.form("gs_expense_form", clear_on_submit=True):
            amt  = st.number_input("Amount ($)", min_value=0.01, format="%.2f", key="gs_amt")
            cat  = st.selectbox(
                "Category",
                ["Food","Transport","Utilities","Entertainment","Rent","Other"],
                key="gs_cat"
            )
            note = st.text_input("Note (optional)", key="gs_note")
            if st.form_submit_button("Add Expense"):
                st.session_state.expenses_list.append({
                    "amount": amt, "category": cat, "note": note
                })

        if st.session_state.expenses_list:
            df    = pd.DataFrame(st.session_state.expenses_list)
            total = df["amount"].sum()
            st.dataframe(df[["category","amount","note"]])
            st.markdown(f"**Total Expenses Added:** ${total:.2f}")

    # ─── Step 4: Savings & Debt ───────────────────────────────────────────────────
    elif st.session_state.step == 3:
        st.session_state.savings = st.number_input(
            "Current Savings ($)",
            min_value=0.0,
            format="%.2f",
            value=st.session_state.savings
        )
        st.session_state.debt    = st.number_input(
            "Current Debt ($)",
            min_value=0.0,
            format="%.2f",
            value=st.session_state.debt
        )

    # ─── Step 5: Summary & AI Advice ──────────────────────────────────────────────
    elif st.session_state.step == 4:
        total_expenses = sum(item["amount"] for item in st.session_state.expenses_list)

        st.subheader("Your Financial Snapshot")
        st.markdown(f"- **Income:**  ${st.session_state.income:,.2f}")
        st.markdown(f"- **Expenses:** ${total_expenses:,.2f}")
        st.markdown(f"- **Savings:**  ${st.session_state.savings:,.2f}")
        st.markdown(f"- **Debt:**     ${st.session_state.debt:,.2f}")
        st.markdown("#### Investment Goals")
        st.markdown(
            f"- 1 Month: ${st.session_state.g1m:,.2f}  \n"
            f"- 3 Months: ${st.session_state.g3m:,.2f}  \n"
            f"- 6 Months: ${st.session_state.g6m:,.2f}  \n"
            f"- 1 Year: ${st.session_state.g1y:,.2f}"
        )

        # donut chart in light theme
        fig = px.pie(
            names=["Income","Expenses","Savings","Debt"],
            values=[
                st.session_state.income,
                total_expenses,
                st.session_state.savings,
                st.session_state.debt
            ],
            hole=0.5,
            title="Financial Breakdown",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

        # AI summary
        if st.button("Get AI Recommendations"):
            st.session_state.ai_advice = ask_financial_profile(
                st.session_state.income,
                st.session_state.g1m,
                st.session_state.g3m,
                st.session_state.g6m,
                st.session_state.g1y,
                total_expenses,
                st.session_state.savings,
                st.session_state.debt
            )

        if st.session_state.ai_advice:
            st.subheader("AI Budget Plan & Tips")
            st.write(st.session_state.ai_advice)

        # Save profile + immediate rerun
        if st.button("Save Profile"):
            add_financial_profile(
                st.session_state.income,
                st.session_state.g1m,
                st.session_state.g3m,
                st.session_state.g6m,
                st.session_state.g1y,
                total_expenses,
                st.session_state.savings,
                st.session_state.debt
            )
            st.success("Profile saved!")
            # attempt to force a rerun, but if not available, swallow the AttributeError
            try:
                st.experimental_rerun()
            except AttributeError:
                pass

        # Return home
        st.button("Return to Dashboard", on_click=go_to_dashboard)

    # ─── Navigation Buttons ───────────────────────────────────────────────────────
    cols = st.columns(2)
    if st.session_state.step > 0:
        cols[0].button("← Back", on_click=prev_step)
    if st.session_state.step < len(steps) - 1:
        cols[1].button("Next →", on_click=next_step)
