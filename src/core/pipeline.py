"""Runs the agents in order and assembles the final report."""

import asyncio
from collections.abc import Callable
from dataclasses import dataclass

from src.core.brief import AccountBrief
from src.core.llm import LLM, AgentOutput, Source

Progress = Callable[[str, float], None]


@dataclass
class Report:
    briefing: str
    sources: list[Source]

    def markdown(self) -> str:
        if not self.sources:
            return self.briefing
        listed = "\n".join(f"{i}. [{s.title}]({s.url})" for i, s in enumerate(self.sources, 1))
        return f"{self.briefing}\n\n## Sources\n\n{listed}\n"


async def generate_report(llm: LLM, brief: AccountBrief, progress: Progress = lambda message, done: None) -> Report:
    # Imported here so the agents package can import from src.core without a cycle.
    from src.agents import AccountAgent, BriefingAgent, CompetitorAgent, ProductAgent, StakeholderAgent

    context: dict[str, AgentOutput] = {}

    progress("Summarising your product", 0.1)
    context["product"] = await ProductAgent().run(llm, brief, context)

    # The three research agents only need the product summary, so they run at the same time.
    researchers = [AccountAgent(), StakeholderAgent()]
    if brief.competitor_urls:
        researchers.append(CompetitorAgent())
    progress("Researching the account, its people" + (" and your competitors" if brief.competitor_urls else ""), 0.3)
    results = await asyncio.gather(*(agent.run(llm, brief, context) for agent in researchers))
    context.update({agent.name: result for agent, result in zip(researchers, results)})

    progress("Writing the briefing", 0.8)
    briefing = await BriefingAgent().run(llm, brief, context)

    sources = list({s.url: s for result in results for s in result.sources}.values())
    progress("Done", 1.0)
    return Report(briefing=briefing.text, sources=sources)
