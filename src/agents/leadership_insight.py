from src.agents.base import Agent
from src.core.llm import LLM


class LeadershipInsightAgent(Agent):
    """
    A specialized agent that generates leadership insights.
    """
    def __init__(self, company_url: str):
        super().__init__("LeadershipInsightAgent")
        self.company_url = company_url

    async def generate(self, llm: LLM, **kwargs) -> str:
        """
        Generate insights using the provided LLM instance.
        This agent is tasked to generate leadership insights.
        """
        summary = kwargs.get("summary")
        prompt = (
            f"You are analyzing the leadership of a company. The company you are assessing is {self.company_url}. "
            f"The strategy team has provided you with the following summary of a product from this company: "
            f"{summary}. \n\n"
            "Using this information, generate insights into the company's leadership, focusing on key leaders "
            "and their connection to the product strategy. \n\n"
            "Your response should include:\n"
            "1. Key leaders and their roles within the company.\n"
            "2. Their responsibilities and involvement in shaping the product strategy.\n"
            "3. Any relevant public statements they have made in the last year related to the product or "
            "company vision. \n\n"
            "Provide a well-structured, insightful analysis that highlights the impact of leadership on the company's "
            "strategic direction.\n\n"
            "At the end of your response, include a 'References' section listing all sources used for your analysis."
        )
        return await llm.generate_insight_async(prompt)