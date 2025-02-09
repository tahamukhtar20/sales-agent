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
        st.session_state.current_page = self.title.lower().replace(" ", "_")
        self.render()
        if st.sidebar.button("Create New Analysis"):
            st.session_state.current_page = "analyze"
            st.rerun()
        if st.sidebar.button("View Previous Analytics"):
            st.session_state.current_page = "records"
            st.rerun()
        st.write("To get started, select an option from the sidebar.")
        if st.session_state.current_page != "landing":
            st.button("← Return to Main", on_click=lambda: st.session_state.pop("current_page"))

    def __str__(self):
        return self.title
