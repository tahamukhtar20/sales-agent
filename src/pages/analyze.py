"""
Analyze Page
"""
from urllib.request import urlopen
import streamlit as st
import validators
from .base import Page
from src.LLM import LLM

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
            product_category = st.text_input("Product Category", placeholder="e.g., Cloud Data Platform, AI-powered Analytics")
            competitor_urls = st.text_area("Competitor URLs (one per line)", placeholder="Enter competitor website URLs, each on a new line")
            value_proposition = st.text_area("Value Proposition", placeholder="Describe why your product is valuable")
            target_customer = st.text_input("Target Customer", placeholder="Enter the name or title of the person you are trying to sell to")
            uploaded_file = st.file_uploader("Upload Product Overview (Optional)", type=["pdf", "docx", "txt"])

        if st.button("Analyze", disabled=st.session_state.analyzing):
            st.session_state.analyzing = True
            self._analyze(product_name, company_url, product_category, competitor_urls, value_proposition, target_customer, uploaded_file)
            st.session_state.analyzing = False

    def _analyze(self, product_name, company_url, product_category, competitor_urls, value_proposition, target_customer, uploaded_file):
        """
        Analyze the inputs provided by the user.
        """
        with st.status("Analyzing...", expanded=True):
            progress = st.progress(0)
            st.write("🔍 Analyzing your product details...")
            if not self._validate_inputs(product_name, company_url, product_category, competitor_urls, value_proposition, target_customer):
                st.session_state.analyzing = False
                return
            progress.progress(0.25)
            llm = LLM(st.session_state.llm_api_key)
            insights = llm.generate_analytics(product_name, company_url, product_category, competitor_urls, value_proposition, target_customer, uploaded_file)
        if insights:
            progress.progress(1.0)
            st.write("📄 Download the analysis report:")
            st.markdown(f"[Download Analysis Report](data:application/pdf;base64,{insights})")
        st.success("🎉 Analysis complete!")

    def _validate_inputs(self, product_name, company_url, product_category, competitor_urls, value_proposition, target_customer):
        """
        Validate the inputs provided by the user.
        Returns True if all inputs are valid, False otherwise.
        """
        if not product_name:
            st.error("Please enter a product name.")
            return False
        if not company_url or not self._validate_url(company_url):
            st.error("Please enter a valid company URL.")
            return False
        if not product_category:
            st.error("Please enter a product category.")
            return False
        if competitor_urls:
            for url in competitor_urls.splitlines():
                if not self._validate_url(url):
                    st.error(f"Invalid competitor URL: {url}")
                    return False
        if not value_proposition:
            st.error("Please enter a value proposition.")
            return False
        if not target_customer:
            st.error("Please enter a target customer.")
            return False
        return True

    def _validate_url(self, url):
        """Validate the given URL."""
        if not url:
            return False
        if validators.url(url):
            try:
                urlopen(url, timeout=5)
                return True
            except:
                return False
        return False
