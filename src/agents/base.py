from abc import ABC, abstractmethod

from src.core.brief import AccountBrief
from src.core.llm import LLM, AgentOutput

# Shared by every research agent: Claude cites with web search, and we build the source
# list from those citations, so the model must not write its own.
RESEARCH_RULES = (
    "Use web search to verify every factual claim and rely on what you find, not on memory. "
    "Prefer primary sources (the company's own site, press releases, filings, earnings calls, job postings) "
    "and information from the last 12 months. If you can't find something, say so instead of guessing. "
    "Don't write a references or sources section; citations are collected automatically. "
    "Write in Markdown with short headings and bullet points, and don't add any preamble."
)


class Agent(ABC):
    """One step of the pipeline: a role (system prompt), a task (prompt) and whether it searches."""

    name: str
    system: str
    web_search = False
    effort = "medium"

    @abstractmethod
    def prompt(self, brief: AccountBrief, context: dict[str, AgentOutput]) -> str:
        """The task for this run, built from the brief and earlier agents' outputs."""

    async def run(self, llm: LLM, brief: AccountBrief, context: dict[str, AgentOutput]) -> AgentOutput:
        return await llm.run(self.system, self.prompt(brief, context), web_search=self.web_search, effort=self.effort)
