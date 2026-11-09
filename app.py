import os

import streamlit as st
from dotenv import load_dotenv

from src.pages import Analyze, Landing

load_dotenv()
st.set_page_config(page_title="Sales Agent", page_icon="📊", layout="centered")

st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY")
st.session_state.setdefault("current_page", "landing")

pages = {"landing": Landing("Landing"), "analyze": Analyze("Analyze")}
pages.get(st.session_state.current_page, pages["landing"])()
