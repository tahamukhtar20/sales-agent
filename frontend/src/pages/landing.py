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
        st.write("Welcome to the Sales Agent Analytics Platform!")
        st.write("This platform is designed to help you analyze and visualize sales data.")
        st.write("Please select an option from the sidebar to get started.")
