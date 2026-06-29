import streamlit as st

# Import page modules
from descriptive import descriptive_page
from diagnostic import diagnostic_page
from predictive import predictive_page
from prescriptive import prescriptive_page
from utils import load_dataset
from statistical_tests import statistical_tests_page  # <--- new page

# ---------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="AI Tools Usage Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------
# PROFESSIONAL LIGHT THEME (Blue + White) - central CSS
# ---------------------------------------------------------------------
# ================================
# GLOBAL UI THEME (INLINE CSS)
# ================================
st.markdown("""
<style>

/* Full page background */
html, body, .stApp {
    background-color: #000000 !important;     /* Black page background */
    color: #FFFFFF !important;                /* White text */
}

/* Main content container */
.main .block-container {
    background-color: transparent !important;
    color: white !important;
}

/* Sidebar (keep your previous theme) */
section[data-testid="stSidebar"] {
    background-color: #f8f9fa !important;     /* Light background */
}

section[data-testid="stSidebar"] * {
    color: #1a1a1a !important;                /* Dark text */
    font-weight: 600 !important;
}

/* ----------------------------
   Dropdown / Select styling
---------------------------- */
div[data-baseweb="select"] * {
    color: white !important;                  /* White text inside dropdown */
}

div[data-baseweb="select"] {
    background-color: #1c1c1c !important;     /* Dark dropdown box */
    border: 1px solid #4c8bf5 !important;     /* Blue border */
    border-radius: 6px !important;
}

div[data-baseweb="popover"] {
    background-color: #1c1c1c !important;     /* Dark dropdown popup */
    color: white !important;
}

/* Dropdown list items */
ul[role="listbox"] li {
    background-color: #1c1c1c !important;
    color: white !important;
}

/* Dropdown hover */
ul[role="listbox"] li:hover {
    background-color: #4c8bf5 !important;
    color: black !important;
}

/* ----------------------------
   Headings & texts
---------------------------- */
h1, h2, h3, h4, h5, h6 {
    color: white !important;
    font-weight: 800 !important;
}

.stMarkdown {
    color: white !important;
}

/* ----------------------------
   Buttons
---------------------------- */
.stButton > button {
    background-color: #4c8bf5 !important; 
    color: white !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.2rem !important;
}

.stButton > button:hover {
    background-color: #1f6fe0 !important;
}

/* ----------------------------
   Tables / DataFrames
---------------------------- */
.dataframe {
    color: white !important;
}

.stDataFrame, .stTable {
    color: white !important;
}

/* Table Headers */
thead th {
    background-color: #2b2b2b !important;
    color: white !important;
}

/* Table Rows */
tbody tr {
    background-color: #1a1a1a !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------------------
st.sidebar.title("AI Tools Analytics")
st.sidebar.write("Select an analytics module:")

menu = st.sidebar.radio(
    "",
    [
        "Home",
        "Descriptive Analytics",
        "Diagnostic Analytics",
        "Predictive Analytics",
        "Prescriptive Analytics",
        "Statistical Tests"   # <-- newly added
    ],
    index=0
)

# ---------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------
def home_page():
    st.title("AI Tools Usage Analytics Platform")
    st.markdown(
        """
        This dashboard provides a complete analytics suite for understanding how students use AI tools.
        
        Sections:
        - Descriptive Analytics — overview and distributions.
        - Diagnostic Analytics — PCA and root-cause analysis.
        - Predictive Analytics — train & evaluate models.
        - Prescriptive Analytics — recommendations and strategy.
        - Statistical Tests — run Chi-square and t-tests.
        
        The dataset is loaded automatically from the configured path.
        """
    )
    st.info("Use the sidebar to navigate through the different analytics modules.")

# ---------------------------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------------------------
if menu == "Home":
    home_page()

elif menu == "Descriptive Analytics":
    descriptive_page()

elif menu == "Diagnostic Analytics":
    diagnostic_page()

elif menu == "Predictive Analytics":
    predictive_page()

elif menu == "Prescriptive Analytics":
    prescriptive_page()

elif menu == "Statistical Tests":
    statistical_tests_page()
