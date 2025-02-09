"""
Base class for all Streamlit pages
"""
import streamlit as st

class Page:
    """
    Base class for all Streamlit pages
    """
    def __init__(self, title: str):
        self.title = title

    def render(self):
        """
        Render the page content
        """
        raise NotImplementedError

    def __call__(self):
        if st.session_state.current_page != "landing":
            st.button("← Return to Main", on_click=lambda: st.session_state.pop("current_page"))
        st.session_state.current_page = self.title.lower().replace(" ", "_")
        self.render()

    def __str__(self):
        return self.title
