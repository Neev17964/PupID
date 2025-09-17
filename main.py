import streamlit as st

import os
import logging
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'     # Suppress TF warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'    # Stop oneDNN startup spam

# Suppress warnings
warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)

from chatbot import show_chat_bot
show_chat_bot()

# 🎯 Streamlit Front Page
st.set_page_config(
    page_title="PupID - Dog Breed Classifier",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #16213e 0%, #1a237e 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* Selectbox container */
    div[data-baseweb="select"] {
        background: linear-gradient(135deg, #0a0f2e 0%, #10163d 100%) !important;
        border-radius: 12px !important;
        padding: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    /* Inside selected value area */
    div[data-baseweb="select"] div[data-baseweb="single-value"] {
        color: #fff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        background: transparent !important;
        opacity: 1 !important;
    }
    /* Selectbox dropdown arrow */
    div[data-baseweb="select"] svg {
        color: white !important;
        fill: white !important;
    }
    /* Selectbox placeholder and input area */
    div[data-baseweb="select"] input, 
    div[data-baseweb="select"] div[data-baseweb="input"] {
        color: #fff !important;
        background: transparent !important;
        font-weight: 600 !important;
    }
    /* Ensure all select text is visible */
    div[data-baseweb="select"] span {
        color: #fff !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }
    /* Dropdown menu */
    div[role="listbox"] {
        background: linear-gradient(135deg, #0a0f2e 0%, #10163d 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    /* Dropdown options */
    div[role="option"] {
        color: white !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    /* Hover and selected effect on options */
    div[role="option"]:hover, 
    div[role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, #8b45db 0%, #2196f3 100%) !important;
    }
    /* Remove unwanted blur/fade/opacity tricks */
    [data-testid="stSidebar"] .stSelectbox * {
        color: #fff !important;
        opacity: 1 !important;
        visibility: visible !important;
        background: transparent !important;
    }
    /* Sidebar title */
    .sidebar-title {
        font-family: Inter, sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b45db 0%, #2196f3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        padding: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">📌 Select a page</p>', unsafe_allow_html=True)
    if 'sidebar_selection' not in st.session_state:
        st.session_state.sidebar_selection = "🏠 Home"
    menu = st.selectbox(
        "🔽 Choose a page",
        options=[
            "🏠 Home",
            "🐕 Breed Predictor",
            "🛍️ Dog Products",
            "ℹ️ About Us"
        ],
        index=[
            "🏠 Home",
            "🐕 Breed Predictor",
            "🛍️ Dog Products",
            "ℹ️ About Us"
        ].index(st.session_state.sidebar_selection),
        label_visibility="collapsed",
        key="sidebar_select"
    )


# Home Page
if menu == "🏠 Home":
    from home_page import show_home_page
    show_home_page()

# Breed Predictor Page
elif menu == "🐕 Breed Predictor":
    from breed_predict_page import show_breed_predict_page
    show_breed_predict_page()

# Dog Products Page
elif menu == "🛍️ Dog Products":
    from Dog_products_page import show_Dog_products_page
    show_Dog_products_page()

# About Page
elif menu == "ℹ️ About Us":
    from About_Us import show_about_us_page
    show_about_us_page()

# Footer
footer = """
<style>
footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 0;
    width: 100vw;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
    z-index: 999999999;
    pointer-events: auto;
}
.footer-icons {
    text-align: center;
}
.footer-icons a {
    margin: 0 15px;
    text-decoration: none;
    display: inline-block;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.footer-icons a:hover {
    transform: scale(1.2);
    box-shadow: 0 0 12px #ffffff88;
}
.footer-icons img {
    width: 30px;
    height: 30px;
    vertical-align: middle;
}
</style>

<footer>
    <div class="footer-icons">
        <a href="https://github.com/Neev17964" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" alt="GitHub">
        </a>
        <a href="https://www.instagram.com/its_neevs/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram">
        </a>
        <a href="https://www.linkedin.com/in/neevsharma" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">
        </a>
    </div>
</footer>
"""

st.markdown(footer, unsafe_allow_html=True)