"""
Landing page for the Sales Agent Analytics Platform
"""
import streamlit as st
from .base import Page

class Landing(Page):
    """
    Landing page for the Sales Agent Analytics Platform
    Contains the implementation of the following methods:
    - render
    """

    def render(self):
        st.set_page_config(page_title="Sales Agent Analytics", page_icon="📊", layout="centered")

        st.title("📊 Sales Agent Analytics")
        st.subheader("Unlock powerful insights and make data-driven sales decisions.")
        st.write("The Sales Agent Analytics Platform is an AI-powered tool designed to help sales representatives gain deep insights into their target accounts. By leveraging advanced GPT models, it analyzes company strategies, competitor activities, and industry trends to provide a data-driven approach to sales. With a user-friendly interface, automated research capabilities, and intelligent recommendations, this platform empowers sales teams to make informed decisions and close deals more effectively. 🚀")

        if st.button("🚀 Create New Analysis", help="Start a new sales data analysis"):
            st.session_state.current_page = "analyze"
            st.rerun()
