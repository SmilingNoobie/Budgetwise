import streamlit as st
import streamlit.components.v1 as components

# ─── 1) PAGE CONFIG ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BudgetWise",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ─── 2) THEME TOGGLE ──────────────────────────────────────────────────────────
def toggle_theme():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    dark = st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.rerun()

    # Base light theme styles
    base_style = """
        [data-testid="stAppViewContainer"] {
            background-color: white;
            color: #31333F;
        }
    """

    # Dark theme overrides
    dark_style = """
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117;
            color: white !important;
        }
        .stButton>button, .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: #2d3436 !important;
            color: white !important;
            border-color: #454e56 !important;
        }
        .stRadio div[role="radiogroup"] > label > div:first-child {
            background-color: #2d3436 !important;
        }
    """

    st.markdown(f"""
        <style>
            {base_style}
            {dark_style if st.session_state.dark_mode else ""}
            .block-container {{
                padding-top: 2rem;
            }}
            @media (max-width: 768px) {{
                .block-container {{ padding: 1rem !important; }}
            }}
            [data-testid="stAppViewContainer"] {{ 
                animation: fadeIn 0.5s ease-in-out; 
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            #MainMenu, .css-1n76uvr, .css-1h3v4to, .css-18e3th9 {{ visibility: hidden; }}
        </style>
    """, unsafe_allow_html=True)


toggle_theme()

# ─── 3) PWA INJECTION ─────────────────────────────────────────────────────────
st.markdown("""
    <link rel="manifest" href="/static/manifest.json" />
    <script>
        if ("serviceWorker" in navigator) {
            window.addEventListener("load", () =>
                navigator.serviceWorker.register("/static/service-worker.js")
            );
        }
    </script>
""", unsafe_allow_html=True)

# ─── 4) IMPORT & INIT ─────────────────────────────────────────────────────────
from components.db import create_table
from views import dashboard, finance_tracker, suggestions, stock_tracker, chatbot

create_table()

# ─── 5) TITLE & NAV ───────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center;'>💸 BudgetWise – Personal Finance & AI Tracker</h1>", unsafe_allow_html=True)

PAGES = {
    "📊 Dashboard": dashboard,
    "➕ Add Expense": add_expense,
    "💡 Budget Suggestions": suggestions,
    "📈 Stock Tracker": stock_tracker,
    "🤖 AI Chatbot": chatbot
}

with st.sidebar:
    st.image("static/icon.png", width=100)
    st.title("BudgetWise")
    selection = st.radio("Navigate", list(PAGES.keys()))

PAGES[selection].run()

# ─── 6) SWIPE NAVIGATION ───────────────────────────────────────────────────────
components.html("""
<script>
let startX, endX, threshold=50;
const radios=[...document.querySelectorAll('input[type=radio]')];
function move(dir){
  let i=radios.findIndex(r=>r.checked);
  radios[(i+dir+radios.length)%radios.length].click();
}
document.addEventListener('touchstart',e=>startX=e.changedTouches[0].screenX);
document.addEventListener('touchend',e=>{
  endX=e.changedTouches[0].screenX;
  if(endX<startX-threshold) move(1);
  if(endX>startX+threshold) move(-1);
});
</script>
""", height=0)