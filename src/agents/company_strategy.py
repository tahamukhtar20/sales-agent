from src.agents.base import Agent
from src.core.llm import LLM


class CompanyStrategyAgent(Agent):
    """
    A specialized agent that generates company strategy insights.
    """
    def __init__(self, company_url: str, product_category: str):
        super().__init__("CompanyStrategyAgent")
        self.company_url = company_url
        self.product_category = product_category

    async def generate(self, llm: LLM, **kwargs) -> str:
        """
        Generate insights using the provided LLM instance.
        This agent is tasked to generate company strategy.
        """
        summary = kwargs.get("summary")
        competitor_analysis = kwargs.get("competitor_analysis")
        leadership_insight = kwargs.get("leadership_insight")
        product_summary = kwargs.get("product_summary")
        prompt = (
            f"You are a sales intelligence assistant helping a sales representative prepare for a meeting with a potential client. "
            f"The target company operates in the {self.product_category} industry and has its main website at {self.company_url}. "
            f"Your goal is to generate a concise, **one-page sales intelligence report** summarizing key strategic insights.\n\n"

            "### **1. Company Strategy Overview**\n"
            f"{summary}\n\n"

            "### **2. Competitor Mentions**\n"
            f"{competitor_analysis}\n\n"

            "### **3. Leadership Insights**\n"
            f"{leadership_insight}\n\n"

            "### **4. Product & Strategy Summary**\n"
            f"{product_summary}\n\n"

            "**Analysis Instructions:**\n"
            "- Add small table where it is really needed, otherwise don't."
            "- Keep the report under **one page (300-400 words)**.\n"
            "- Use a structured, easy-to-read format.\n"
            "- Highlight **public statements, press releases, or job postings** that indicate the company’s strategic direction.\n"
            "- Identify any key leaders (e.g., Chief Data Officer, Chief Compliance Officer) and their relevance to the sales conversation.\n"
            "- If available, summarize insights from **10-Ks, annual reports, or industry reports**.\n\n"
            "- Should be in headings and description format."
            "- Do use direct names for more legitimacy."

            "**References:**\n"
            "Include a 'References' section at the end, listing all sources used. If you received links from the above "
            "details, add those in the references as well. Do add explicit links along side other references.\n"
            "**Do not include any introductory text or explanations—output only the report**."

            "**Return the formatted report text as-is, without any prefatory statements, disclaimers, or summaries.**"
        )

        return await llm.generate_insight_async(prompt)
