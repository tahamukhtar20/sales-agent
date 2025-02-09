"""
Past Insights are found on this page
"""
import streamlit as st
from .base import Page

class Records(Page):
    """
    Records page for the Sales Agent Analytics Platform
    Contains the implementation of the following methods:
    - render
    """
    def render(self):
        st.write("Welcome to the Records Page!")
        st.write("This page is designed to help you view and analyze past sales data.")
        st.write("Please select an option from the sidebar to get started.")
