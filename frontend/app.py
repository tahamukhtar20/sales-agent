"""
This file is the main file for the frontend. It will be used to create the web app using Streamlit.
"""
import streamlit as st
from src.pages import Landing, Records, Analyze

if __name__ == "__main__":
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"

    pages = {
        "landing": Landing("Landing"),
        "records": Records("Records"),
        "analyze": Analyze("Analyze"),
    }

    page = pages.get(
        st.session_state.current_page,
        pages["landing"]
    )

    page()
