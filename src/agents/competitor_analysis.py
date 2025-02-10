from src.agents.base import Agent
from src.core.llm import LLM


class CompetitorAnalysisAgent(Agent):
    def __init__(self, competitor_urls: list):
        super().__init__("CompetitorAnalysisAgent")
        self.competitor_urls = competitor_urls
        self.summary = None

    async def generate(self, llm: LLM, **kwargs) -> str:
        competitors = ", ".join(self.competitor_urls)
        summary = kwargs.get("summary")
        prompt = (
            f"You are a project management agent at a software company. Your product has the following summary: {summary}. "
            f"You have been provided with the following list of competitor URLs: {competitors}. \n\n"
            "Your task is to analyze the competition and generate a structured summary, including:\n"
            "1. An overview of each competitor's product offerings.\n"
            "2. Their target market and customer segments.\n"
            "3. Their unique selling points (USPs) and competitive differentiators.\n\n"
            "Ensure your analysis is data-driven and well-structured. At the end of your response, "
            "include a References section listing all sources used for your analysis."
        )

        return await llm.generate_insight_async(prompt)
