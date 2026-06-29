import streamlit as st
from descriptive import descriptive_page
from diagnostic import diagnostic_page
from predictive import predictive_page
from decisive import decisive_page
from prescriptive import prescriptive_page

# ---------------------------------------------------
# GLOBAL THEME: Blue + White + Light Gray
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Theme
theme_css = """
<style>
/* Global Background */
body {
    background-color: #f2f5f9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #e8edf5;
}

/* Header style */
h1, h2, h3 {
    color: #003366 !important;
    font-weight: 700 !important;
}

/* Cards */
div[data-testid="stMetric"] {
    background-color: white;
    border: 2px solid #d6ddec;
    border-radius: 10px;
    padding: 15px;
}

/* Buttons */
.stButton>button {
    background-color: #003366;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #0059b3;
}

/* Sidebar buttons */
div[data-testid="stSidebarNav"] button {
    background-color: #003366;
    color: white;
    border-radius: 6px;
}
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------
st.sidebar.title("📘 AI Analytics Dashboard")
st.sidebar.markdown("### Choose an analytics type:")

page = st.sidebar.radio(
    "",
    [
        "📊 Descriptive Analytics",
        "🔍 Diagnostic Analytics",
        "🔮 Predictive Analytics",
        "🧭 Decisive Analytics",
        "💡 Prescriptive Analytics"
    ]
)

# ---------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------
if page == "📊 Descriptive Analytics":
    descriptive_page()

elif page == "🔍 Diagnostic Analytics":
    diagnostic_page()

elif page == "🔮 Predictive Analytics":
    predictive_page()

elif page == "🧭 Decisive Analytics":
    decisive_page()

elif page == "💡 Prescriptive Analytics":
    prescriptive_page()
