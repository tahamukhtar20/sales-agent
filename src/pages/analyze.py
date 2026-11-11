import asyncio
import os
import tempfile

import anthropic
import streamlit as st
from markdown_pdf import MarkdownPdf, Section

from ..core import LLM, AccountBrief, RefusalError, generate_report, limits
from ..core.documents import SUPPORTED, extract_text
from .base import Page


class Analyze(Page):
    """The form, the run, and the finished brief."""

    def render(self):
        st.title("New account brief")
        st.write("Tell us what you sell and who you're meeting. The agents research the rest.")

        with st.form("brief"):
            st.subheader("Your product")
            product_name = st.text_input("Product name", placeholder="e.g. Acme Data Cloud")
            product_category = st.text_input("Category", placeholder="e.g. Cloud data platform")
            value_proposition = st.text_area("Value proposition", placeholder="Why customers buy it, in a few sentences")
            competitor_urls = st.text_area(
                "Competitor websites (optional, one per line)", placeholder="https://competitor.example"
            )
            document = st.file_uploader(
                "Product overview (optional)", type=[ext.lstrip(".") for ext in SUPPORTED]
            )

            st.subheader("The account")
            account_url = st.text_input("Company website", placeholder="https://prospect.example")
            contact_role = st.text_input("Who you're meeting", placeholder="A name or a job title, e.g. Chief Data Officer")

            submitted = st.form_submit_button("Research and write the brief", type="primary")

        if not submitted:
            return

        try:
            notes = extract_text(document, document.name) if document else ""
        except ValueError as e:
            st.error(str(e))
            return

        brief = AccountBrief(
            product_name=product_name.strip(),
            product_category=product_category.strip(),
            value_proposition=value_proposition.strip(),
            competitor_urls=[u.strip() for u in competitor_urls.splitlines() if u.strip()],
            product_notes=notes,
            account_url=account_url.strip(),
            contact_role=contact_role.strip(),
        )
        if problems := brief.errors():
            for problem in problems:
                st.error(problem)
            return

        if not st.session_state.get("api_key"):
            st.error("No Anthropic API key is configured. Set ANTHROPIC_API_KEY and restart the app.")
            return

        if reason := limits.check():
            st.warning(reason)
            return
        limits.record()
        self._run(brief)

    @staticmethod
    def _run(brief: AccountBrief):
        llm = LLM(api_key=st.session_state.api_key)
        with st.status("Working on it…", expanded=True) as status:
            bar = st.progress(0.0)

            def progress(message: str, done: float):
                bar.progress(done)
                if done < 1:
                    st.write(message)

            try:
                report = asyncio.run(generate_report(llm, brief, progress))
            except RefusalError as e:
                status.update(label="Stopped", state="error")
                st.error(str(e))
                return
            except anthropic.AuthenticationError:
                status.update(label="Stopped", state="error")
                st.error("The Anthropic API key was rejected.")
                return
            except anthropic.RateLimitError:
                status.update(label="Stopped", state="error")
                st.error("Rate limited by the API. Wait a minute and try again.")
                return
            except (anthropic.APIStatusError, anthropic.APIConnectionError) as e:
                status.update(label="Stopped", state="error")
                st.error(f"The API request failed: {e}")
                return
            status.update(label="Brief ready", state="complete", expanded=False)

        with st.expander("Research log"):
            for name, searches, found, cited, errors in report.log:
                line = f"**{name}**: {searches} searches, {found} pages found, {cited} cited"
                if errors:
                    line += f"; failed searches: {', '.join(errors)}"
                st.markdown(line)

        markdown = report.markdown()
        st.download_button(
            "Download as PDF", data=Analyze._pdf(markdown), file_name="account-brief.pdf", mime="application/pdf"
        )
        st.markdown(markdown)

    @staticmethod
    def _pdf(markdown: str) -> bytes:
        pdf = MarkdownPdf()
        pdf.meta["title"] = "Account brief"
        pdf.add_section(Section(markdown, toc=False))
        fd, path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)
        try:
            pdf.save(path)
            with open(path, "rb") as f:
                return f.read()
        finally:
            os.remove(path)
