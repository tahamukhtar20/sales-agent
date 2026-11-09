import streamlit as st


class Page:
    """A screen of the app. Subclasses implement render()."""

    def __init__(self, title: str):
        self.title = title

    def render(self):
        raise NotImplementedError

    def __call__(self):
        if st.session_state.current_page != "landing":
            st.button("← Back", on_click=lambda: st.session_state.update(current_page="landing"))
        self.render()

    def __str__(self):
        return self.title
