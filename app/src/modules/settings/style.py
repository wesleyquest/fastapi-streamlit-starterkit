import streamlit as st
import base64
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
"""
account_img_path = r'/app/src/images/account.png'
logout_img_path = r'/app/src/images/logout.png'
description_img_path = r'/app/src/images/description.png'
with open(account_img_path, "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode('utf-8')
with open(logout_img_path, "rb") as image_file:
    logout_img = base64.b64encode(image_file.read()).decode('utf-8')
with open(description_img_path, "rb") as image_file:
    description_img = base64.b64encode(image_file.read()).decode('utf-8')
"""
#style
def style_global():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css?family=Gothic+A1:100,400');

        .main > .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        div.stButton {
                text-align:center;
            }
        div.stSpinner > div {
        text-align:center;
        align-items: center;
        justify-content: center;
        }
        .stApp header {
                z-index: 1;
                background: transparent;
        }
        .st-d4.st-b8.st-d5 {
        width: 30%;
        }
        .navbar {
        position: fixed;
        top: 2px;
        left: 0px;
        width: 100%;
        padding: 0px;
        z-index: 1;
        padding-left: 20px;
        padding-right: 20px;
        background: #3D52A0;
        height: 50px;
        }
        .box {
        margin: auto;
        width: 100%;
        padding: 10px;
        text-align: center;
        color: white;
        font-size: 20px;
        }
        </style>""", unsafe_allow_html=True)


    st.markdown(f"""
    <nav class="navbar">
        <div class="box"> 
            <span style="font-family:'Space Grotesk'">{APP_NAME} </span>
            <span style="font-size: 15px;font-family:'Space Grotesk'"> {APP_VERSION} </span>
        </div>
    </nav>
        """, unsafe_allow_html=True)
    
