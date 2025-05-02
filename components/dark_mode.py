# components/dark_mode.py
import streamlit as st

def toggle_theme():
    # Initialize with dark mode ON
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True  # Changed to default True

    dark = st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.rerun()

    # Dark theme (now default)
    dark_style = """
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117 !important;
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
        .st-bb, .st-at, .st-ae, .st-af, .st-ag, .st-ah, .st-ai, .st-aj {
            color: white !important;
        }
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1a1d24 !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: white !important;
        }
    """

    # Light theme
    light_style = """
        [data-testid="stAppViewContainer"] {
            background-color: white;
            color: #31333F;
        }
    """

    st.markdown(f"""
        <style>
            {dark_style if st.session_state.dark_mode else light_style}
            .block-container {{
                padding-top: 2rem;
            }}
            @media (max-width: 768px) {{
                .block-container {{ padding: 1rem !important; }}
            }}
        </style>
    """, unsafe_allow_html=True)