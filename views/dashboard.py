import streamlit as st
import plotly.express   as px
import plotly.graph_objects as go
from components.db      import get_summary, get_latest_profile

def run():
    st.header("Budget Dashboard Overview")

    prof = get_latest_profile()
    if prof is None:
        st.info("No financial profile found. Go to Get Started to set it up.")
        return

    # Profile metrics
    st.subheader("Your Profile")
    st.metric("After‑Tax Income", f"${prof['after_tax_income']:,.2f}")
    c1, c2 = st.columns(2)
    c1.metric("1‑Mo Goal", f"${prof['goal_1m']:,.2f}")
    c2.metric("Savings",  f"${prof['savings']:,.2f}")
    st.markdown("---")

    # This month’s expenses
    total, count, grouped = get_summary()
    remaining = max(prof["after_tax_income"] - total, 0.0)

    # Sankey chart
    st.subheader("Income Flow (Sankey)")
    labels = ["Income"] + grouped["category"].tolist() + ["Remaining"]
    sources = [0]*len(grouped) + [0]
    targets = list(range(1,1+len(grouped))) + [len(grouped)+1]
    values  = grouped["amount"].tolist() + [remaining]
    fig_sankey = go.Figure(go.Sankey(
        node=dict(label=labels, pad=15, thickness=20),
        link=dict(source=sources, target=targets, value=values)
    ))
    fig_sankey.update_layout(template="plotly_white", height=350)
    st.plotly_chart(fig_sankey, use_container_width=True)
    st.markdown("---")

    # Bar chart
    st.subheader("Spending by Category")
    if grouped.empty:
        st.info("No expenses logged yet.")
    else:
        fig_bar = px.bar(
            grouped, x="category", y="amount",
            labels={"amount":"Amount ($)","category":"Category"},
            template="plotly_white",
            color="amount", color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("---")

    # Goal vs actual
    st.subheader("Goal vs. Actual (1‑Month)")
    fig_goal = px.bar(
        x=["1‑Mo Goal","Actual Spending"],
        y=[prof["goal_1m"], total],
        labels={"x":"","y":"Amount ($)"},
        template="plotly_white"
    )
    st.plotly_chart(fig_goal, use_container_width=True)
