"""
Analyze Page
"""
import streamlit as st
from .base import Page
import asyncio
from src.core.report_generator import ReportGenerator
from ..core.llm import LLM


class Analyze(Page):
    """
    Insight Analysis Page
    Contains the implementation of the following methods:
    - render
    - validate_url
    """

    def render(self):
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

        if st.button("Analyze", disabled=st.session_state.analyzing):
            st.session_state.analyzing = True
            asyncio.run(self._analyze(product_name, company_url, product_category, competitor_urls, value_proposition,
                                        target_customer, uploaded_file))
            st.session_state.analyzing = False


    async def _analyze(self, product_name, company_url, product_category, competitor_urls, value_proposition, target_customer,
                 uploaded_file):
        """
        Analyze the inputs provided by the user.
        """
        llm = LLM(model_name="gemini-2.0-flash", api_key=st.session_state.llm_api_key)
        with st.status("Analyzing...", expanded=True):
            progress = st.progress(0)
            st.write("🔍 Analyzing your product details...")
            report_generator = ReportGenerator(llm, product_name=product_name, company_url=company_url, product_category=product_category,
            competitor_urls=competitor_urls, value_proposition=value_proposition, target_customer=target_customer,
            uploaded_file=uploaded_file, progress=progress)
            if not report_generator.validate_inputs():
                st.session_state.analyzing = False
                return
            progress.progress(0.2)
            report_text = await report_generator.generate_report()
            st.write(report_text)

        st.success("🎉 Analysis complete!")

