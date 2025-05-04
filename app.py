import streamlit as st
import streamlit.components.v1 as components

# 1) Must be first
st.set_page_config(
    page_title="BudgetWise",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2) Global styles
st.markdown("""
<style>
  .appview-container, .block-container {background-color: #f5f7fa; font-family:'Segoe UI';}
  h1, h2, h3, .stMetric>div>div>div>h3 {color: #1f77b4 !important;}
  [data-baseweb="radio"] label {font-size:1.1rem !important; line-height:1.5rem;}
  .stButton>button {background-color:#1f77b4!important; color:white!important; border-radius:5px!important;}
  #MainMenu, footer, header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# 3) PWA injection
st.markdown("""
<link rel="manifest" href="/static/manifest.json" />
<script>
 if ("serviceWorker" in navigator) {
   window.addEventListener("load", ()=> navigator.serviceWorker.register("/static/service-worker.js"));
 }
</script>
""", unsafe_allow_html=True)

# 4) Create tables
from components.db import create_table
create_table()

# 5) Import run() from each page
from views.get_started   import run as get_started
from views.dashboard    import run as dashboard
from views.finance_entry  import run as add_expense
from views.stock_tracker import run as stock_tracker
from views.chatbot      import run as chatbot

PAGES = {
    "Get Started":   get_started,
    "Dashboard":     dashboard,
    "Add Expense":   add_expense,
    "Stock Tracker": stock_tracker,
    "AI Chatbot":    chatbot
}

# 6) Header
st.markdown("<h1 style='text-align:center;'>BudgetWise – Personal Finance & AI Tracker</h1>", unsafe_allow_html=True)

# 7) Sidebar nav
if "selection" not in st.session_state:
    st.session_state.selection = "Get Started"

with st.sidebar:
    st.title("🏦 BudgetWise")
    st.radio("Navigate", list(PAGES.keys()), key="selection")

# 8) Run
PAGES[st.session_state.selection]()

# 9) Swipe nav for mobile nav
components.html("""
<script>
 let startX, endX, th=50;
 const r=[...document.querySelectorAll('input[type=radio]')];
 function m(d){ let i=r.findIndex(x=>x.checked); r[(i+d+r.length)%r.length].click() }
 document.addEventListener('touchstart', e=> startX=e.changedTouches[0].screenX);
 document.addEventListener('touchend',   e=>{ endX=e.changedTouches[0].screenX;
   if(endX<startX-th) m(1); if(endX>startX+th) m(-1);
 });
</script>
""", height=0)
