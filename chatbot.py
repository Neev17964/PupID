import streamlit as st
import base64
import os

def show_chat_bot():
    # --- Session toggle for chatbot ---
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    # Load icon image
    def get_base64(bin_file):
        with open(bin_file, "rb") as f:
            return base64.b64encode(f.read()).decode()

    img_path = "CareBot.png"
    if not os.path.exists(img_path):
        st.warning("CareBot.png not found!")
        return

    img_base64 = get_base64(img_path)

    # --- Floating Icon Button ---
    with st.form(key="chat_form", clear_on_submit=False):
        submit = st.form_submit_button(label="", use_container_width=True)

        st.markdown(f"""
            <style>
                [data-testid="stForm"] {{
                    position: fixed;
                    bottom: 50px;
                    right: 20px;
                    width: 60px;
                    height: 60px;
                    padding: 0;
                    margin: 0;
                    background-color: transparent;
                    z-index: 999999999;
                }}
                [data-testid="stForm"] button {{
                    width: 100%;
                    height: 100%;
                    border: none;
                    border-radius: 50%;
                    background-image: url("data:image/png;base64,{img_base64}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                    transition: transform 0.2s ease-in-out;
                }}
                [data-testid="stForm"] button:hover {{
                    transform: scale(1.1);
                }}

                [data-testid="stForm"] {{
                    background-color: transparent !important;
                }}

                [data-testid="stForm"] button {{
                    background-color: transparent !important;
                }}

            </style>
        """, unsafe_allow_html=True)

    # --- Toggle chatbot visibility ---
    if submit:
        st.session_state.chat_open = not st.session_state.chat_open

    # --- Show chatbot iframe if open ---
    if st.session_state.chat_open:
        st.markdown("""
            <iframe
                src="https://www.chatbase.co/chatbot-iframe/T0GT0FTMzkOxXXhbNiAuB"
                style="
                    position: fixed;
                    bottom: 90px;
                    right: 20px;
                    width: 350px;
                    height: 75vh;
                    border: none;
                    border-radius: 12px;
                    z-index: 999999999;
                ">
            </iframe>
        """, unsafe_allow_html=True)
