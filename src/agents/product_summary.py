from src.agents.base import Agent
from src.core.llm import LLM


class ProductSummaryAgent(Agent):
    def __init__(self, product_name: str, company_url: str):
        super().__init__("ProductSummaryAgent")
        self.product_name = product_name
        self.company_url = company_url

    async def generate(self, llm: LLM, **kwargs) -> str:
        summary = kwargs.get("summary")
        competitor_analysis = kwargs.get("competitor_analysis"),
        leadership_insight = kwargs.get("leadership_insight"),
        prompt = (
            f"You are a market research and product strategy analyst. Your task is to analyze the product and strategy of "
            f"{self.product_name}, a company with the following website: {self.company_url}. \n\n"
            "### Product & Strategy Summary\n"
            f"{summary}\n\n"
            "### Competitor Analysis\n"
            f"{competitor_analysis}\n\n"
            "### Leadership Insights\n"
            f"{leadership_insight}\n\n"
            "#### Task:\n"
            "Using the provided information, generate a detailed summary of the company's product strategy. "
            "For public companies, incorporate insights from 10-K reports, annual reports, or other relevant public documents. "
            "For private companies, use available information from their website. \n\n"
            "**Your response should include:**\n"
            "1. A high-level summary of the product and its strategic direction.\n"
            "2. Key differentiators and competitive advantages based on competitor analysis.\n"
            "3. How leadership influences the product strategy, referencing recent statements or decisions.\n\n"
            "**References:**\n"
            "At the end of your response, include a 'References' section listing all sources used in your analysis."
        )
        return await llm.generate_insight_async(prompt)
