import asyncio

import streamlit as st
import validators

from src.agents.company_strategy import CompanyStrategyAgent
from src.agents.competitor_analysis import CompetitorAnalysisAgent
from src.agents.document_parsing import DocumentParsingAgent
from src.agents.leadership_insight import LeadershipInsightAgent
from src.agents.product_summary import ProductSummaryAgent
from src.agents.summary import SummaryAgent
from src.core.llm import LLM


class ReportGenerator:
    """
    Coordinates multiple agents to produce a comprehensive sales insights report,
    then exports it as a PDF.
    """

    def __init__(self, llm: LLM, product_name, company_url, product_category, competitor_urls, value_proposition,
                 target_customer, uploaded_file, progress):
        self.llm = llm
        self.product_name = product_name
        self.company_url = company_url
        self.product_category = product_category
        self.competitor_urls = competitor_urls
        self.value_proposition = value_proposition
        self.target_customer = target_customer
        self.uploaded_file = uploaded_file
        self.progress = progress
        self.summary_agent = SummaryAgent(self.product_name, self.company_url, self.product_category,
                                          self.value_proposition, self.target_customer)
        self.company_strategy_agent = CompanyStrategyAgent(self.product_name, self.company_url)
        self.competitor_analysis_agent = CompetitorAnalysisAgent(
            self.competitor_urls.splitlines()) if self.competitor_urls else None
        self.leadership_insight_agent = LeadershipInsightAgent(self.target_customer)
        self.product_summary_agent = ProductSummaryAgent(self.product_name, self.company_url)
        self.document_parsing_agent = DocumentParsingAgent(self.uploaded_file) if self.uploaded_file else None

    async def generate_report(self) -> str:
        document_text = None
        if self.document_parsing_agent:
            st.write("📄 Parsing your document...")
            document_text = await self.document_parsing_agent.generate(self.llm) if self.document_parsing_agent else ""

        st.write("📝 Generating Summary based on your description...")
        summary = await self.summary_agent.generate(self.llm, document_text=document_text)
        self.progress.progress(0.3)

        st.write("📊 Analyzing Competitors and Leadership insights...")
        competitor_analysis, leadership_insight = await asyncio.gather(
            self.competitor_analysis_agent.generate(self.llm, summary=summary),
            self.leadership_insight_agent.generate(self.llm, summary=summary),
        )
        self.progress.progress(0.4)

        st.write("📈 Analyzing Strategy...")
        product_summary = await self.product_summary_agent.generate(
            self.llm,
            summary=summary,
            competitor_analysis=competitor_analysis,
            leadership_insight=leadership_insight,
        )
        self.progress.progress(0.5)

        st.write("⚙️ Preparing the final report...")
        company_strategy = await self.company_strategy_agent.generate(
            self.llm,
            summary=summary,
            competitor_analysis=competitor_analysis,
            leadership_insight=leadership_insight,
            product_summary=product_summary,
        )
        self.progress.progress(0.6)

        return company_strategy

    def validate_inputs(self):
        """
        Validate the inputs provided by the user.
        Returns True if all inputs are valid, False otherwise.
        """
        if not self.product_name:
            st.error("Please enter a product name.")
            return False
        if not self.company_url or not ReportGenerator._validate_url(self.company_url):
            st.error("Please enter a valid company URL.")
            return False
        if not self.product_category:
            st.error("Please enter a product category.")
            return False
        if self.competitor_urls:
            for url in self.competitor_urls.splitlines():
                if not ReportGenerator._validate_url(url):
                    st.error(f"Invalid competitor URL: {url}")
                    return False
        if not self.value_proposition:
            st.error("Please enter a value proposition.")
            return False
        if not self.target_customer:
            st.error("Please enter a target customer.")
            return False
        return True

    @staticmethod
    def _validate_url(url):
        """Validate the given URL."""
        if not url:
            return False
        if not validators.url(url):
            return False
        return True
