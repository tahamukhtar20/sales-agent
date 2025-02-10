import os
import tempfile

import streamlit as st
from markdown_pdf import MarkdownPdf, Section

from .base import Page
import asyncio
from ..core import LLM, ReportGenerator


class Analyze(Page):
    """
    Insight Analysis Page
    Contains the implementation of the following methods:
    - render
    - validate_url
    """

    def render(self):
        """
        Render the Insight Analysis Page.
        """
        st.title("🔍 Insight Analysis Page")
        st.write("Analyze and gain insights into your target accounts.")

        if "analyzing" not in st.session_state:
            st.session_state.analyzing = False

        with st.expander("🔹 **Enter Product Details**", expanded=not st.session_state.analyzing):
            product_name = st.text_input("Product Name", placeholder="Enter the name of the product you're selling")
            company_url = st.text_input("Company URL", placeholder="Enter the URL of the company you are targeting")
            product_category = st.text_input("Product Category",
                                             placeholder="e.g., Cloud Data Platform, AI-powered Analytics")
            competitor_urls = st.text_area("Competitor URLs (one per line)",
                                           placeholder="Enter competitor website URLs, each on a new line")
            value_proposition = st.text_area("Value Proposition", placeholder="Describe why your product is valuable")
            target_customer = st.text_input("Target Customer",
                                            placeholder="Enter the name or title of the person you are trying to sell to")
            uploaded_file = st.file_uploader("Upload Product Overview (Optional)", type=["pdf", "docx", "txt"])

        if st.button("Analyze"):
            st.session_state.analyzing = True
            asyncio.run(Analyze._analyze(product_name, company_url, product_category, competitor_urls, value_proposition,
                                        target_customer, uploaded_file))
            st.session_state.analyzing = False

    @staticmethod
    async def _analyze(product_name, company_url, product_category, competitor_urls, value_proposition, target_customer,
                       uploaded_file):
        """
        Analyze the inputs provided by the user and generate a PDF report.
        """
        try:
            llm = LLM(model_name="gemini-2.0-flash", api_key=st.session_state.llm_api_key)

            with st.status("🔍 Analyzing...", expanded=True) as status:
                progress = st.progress(0)
                st.write("📊 Processing input data...")

                report_generator = ReportGenerator(
                    llm, product_name=product_name, company_url=company_url, product_category=product_category,
                    competitor_urls=competitor_urls, value_proposition=value_proposition,
                    target_customer=target_customer,
                    uploaded_file=uploaded_file, progress=progress
                )

                if not report_generator.validate_inputs():
                    st.error("⚠️ Invalid inputs! Please check your entries and try again.")
                    st.session_state.analyzing = False
                    return

                progress.progress(0.2)
                report_text = await report_generator.generate_report()
                progress.progress(0.7)

                pdf_data = Analyze._generate_pdf_report(report_text)
                progress.progress(1.0)

                st.success("🎉 Analysis complete! Download your report below.")
                st.download_button(
                    label="📥 Download Report (PDF)",
                    data=pdf_data,
                    file_name="Report.pdf",
                    mime="application/pdf"
                )

                status.update(label="✅ Analysis completed!", state="complete")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.session_state.analyzing = False

    @staticmethod
    def _generate_pdf_report(report_text: str) -> bytes:
        """
        Convert markdown report text to HTML and generate a properly formatted PDF using WeasyPrint.
        """
        pdf = MarkdownPdf()
        pdf.meta["title"] = 'Title'
        pdf.add_section(Section(report_text, toc=False))

        temp_fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        os.close(temp_fd)

        try:
            pdf.save(temp_path)

            with open(temp_path, "rb") as f:
                pdf_bytes = f.read()
        finally:
            os.remove(temp_path)

        return pdf_bytes
