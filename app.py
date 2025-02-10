import streamlit as st
from dotenv import load_dotenv
import os

from src.pages import Landing, Analyze

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if __name__ == "__main__":
    st.session_state.llm_api_key = GEMINI_API_KEY
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"

    pages = {
        "landing": Landing("Landing"),
        "analyze": Analyze("Analyze"),
    }

    page = pages.get(
        st.session_state.current_page,
        pages["landing"]
    )

    page()
