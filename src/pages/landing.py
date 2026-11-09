import streamlit as st

from .base import Page


class Landing(Page):
    def render(self):
        st.title("Sales Agent")
        st.subheader("A one-page brief for your next sales meeting, researched for you.")
        st.write(
            "Describe your product and the company you're meeting. Research agents built on Claude search "
            "the web for the account's priorities, the people you'll meet and how your competitors compare, "
            "then write a brief with talking points. Every fact in the brief comes from a cited source."
        )
        if st.button("Create a brief", type="primary"):
            st.session_state.current_page = "analyze"
            st.rerun()
