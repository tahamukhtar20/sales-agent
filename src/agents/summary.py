from src.agents.base import Agent
from src.core.llm import LLM


class SummaryAgent(Agent):
    """
    A specialized agent that generates a strategic summary of a product.
    """
    def __init__(self, product_name, company_url, product_category, value_proposition, target_customer):
        super().__init__("SummaryAgent")
        self.product_name = product_name
        self.company_url = company_url
        self.product_category = product_category
        self.value_proposition = value_proposition
        self.target_customer = target_customer

    async def generate(self, llm: LLM, **kwargs) -> str:
        """
        Generate insights using the provided LLM instance.
        This agent is tasked to generate a strategic summary of a product.
        """
        document_text = kwargs.get("document_text", "")
        prompt = (
            f"As a product manager agent for the {self.product_name}, in the company {self.company_url}, you are preparing "
            f"a strategic summary to present to the executive board. Below are the key details about the product:\n"
            f"Product Category: {self.product_category}\n"
            f"Value Proposition: {self.value_proposition}\n"
            f"Target Customer: {self.target_customer}\n\n"
            f"Supporting Details: {document_text}\n\n"
            "Please provide a concise and impactful summary of the product strategy, ensuring clarity and persuasion. "
            "The summary must include:\n"
            "1. Core Features – Highlight the most critical functionalities that define the product.\n"
            "2. Unique Selling Points (USPs) – What sets this product apart from competitors?\n"
            "3. Competitive Advantages – Explain the product's market differentiation and strategic edge.\n\n"
            "At the end of the response, include a References section citing all sources used, such as reports, "
            "articles, or market data.\n\n"
            "Tone & Style:\n"
            "- Concise, clear, and professional\n"
            "- Strategic and data-driven\n"
            "- Persuasive yet factual"
        )

        return await llm.generate_insight_async(prompt)
