"""The agents. Two work from what the user gave us; three research the web in parallel."""

from src.agents.base import RESEARCH_RULES, Agent
from src.core.brief import AccountBrief
from src.core.llm import AgentOutput


class ProductAgent(Agent):
    """Turns the seller's inputs (and optional product document) into a crisp product summary."""

    name = "product"
    effort = "low"
    system = (
        "You help sales teams describe their own product clearly. Work only from the material provided; "
        "don't invent features, customers or numbers. Write in Markdown and don't add any preamble."
    )

    def prompt(self, brief: AccountBrief, context: dict[str, AgentOutput]) -> str:
        notes = f"\n\nProduct document:\n<document>\n{brief.product_notes}\n</document>" if brief.product_notes else ""
        return (
            f"{brief.seller_summary()}{notes}\n\n"
            "Summarise this product in under 200 words: what it does, who it's for, its key capabilities "
            "and what sets it apart."
        )


class AccountAgent(Agent):
    """Researches the target company's business and current priorities."""

    name = "account"
    web_search = True
    system = "You are a sales research analyst preparing a seller for a meeting with a prospective customer. " + RESEARCH_RULES

    def prompt(self, brief: AccountBrief, context: dict[str, AgentOutput]) -> str:
        return (
            f"The prospective customer's website is {brief.account_url}.\n\n"
            f"The seller's product:\n{context['product'].text}\n\n"
            "Research this company and report:\n"
            "1. What the company does, its size and its main markets.\n"
            "2. Its strategic priorities and recent moves (launches, partnerships, funding, acquisitions, "
            "restructuring), with dates.\n"
            "3. Signals that relate to the seller's product category, such as relevant job postings, "
            "technology choices or stated challenges.\n"
            "Keep it under 350 words."
        )


class StakeholderAgent(Agent):
    """Researches the people at the target company who matter for this deal."""

    name = "stakeholders"
    web_search = True
    system = "You are a sales research analyst mapping the decision makers at a prospective customer. " + RESEARCH_RULES

    def prompt(self, brief: AccountBrief, context: dict[str, AgentOutput]) -> str:
        return (
            f"The prospective customer's website is {brief.account_url}. "
            f"The seller is meeting: {brief.contact_role}.\n\n"
            f"The seller's product:\n{context['product'].text}\n\n"
            "Report on:\n"
            "1. The person being met (or whoever holds that role): their background and remit.\n"
            "2. Other leaders likely to influence a purchase in this category, with their roles.\n"
            "3. Their public statements from the last 12 months that relate to the seller's product area.\n"
            "Only include people you can verify. Keep it under 300 words."
        )


class CompetitorAgent(Agent):
    """Compares the seller's competitors with the seller's product, from the account's point of view."""

    name = "competitors"
    web_search = True
    system = "You are a competitive intelligence analyst supporting a sales team. " + RESEARCH_RULES

    def prompt(self, brief: AccountBrief, context: dict[str, AgentOutput]) -> str:
        competitors = "\n".join(f"- {url}" for url in brief.competitor_urls)
        return (
            f"The seller's product:\n{context['product'].text}\n\n"
            f"The seller's competitors:\n{competitors}\n\n"
            f"The prospective customer: {brief.account_url}\n\n"
            "For each competitor, report its positioning, target customers and main strengths, then how the "
            "seller's product compares. Note any evidence that the prospective customer already uses one of "
            "these competitors. Keep it under 350 words."
        )


class BriefingAgent(Agent):
    """Writes the final one-page meeting brief from everything the other agents found."""

    name = "briefing"
    effort = "high"
    system = (
        "You write one-page briefs that prepare a salesperson for a first meeting. Use only the research "
        "notes you're given; never add facts that aren't in them. Write in Markdown with short headings, "
        "use a table only where it clearly helps, and don't add a sources section or any preamble."
    )

    def prompt(self, brief: AccountBrief, context: dict[str, AgentOutput]) -> str:
        sections = {
            "product": "The seller's product",
            "account": "The account",
            "stakeholders": "People",
            "competitors": "Competitors",
        }
        notes = "\n\n".join(
            f"## {title}\n{context[key].text}" for key, title in sections.items() if key in context
        )
        return (
            f"Research notes:\n\n{notes}\n\n"
            f"Write a brief (350 to 450 words) for a meeting with {brief.contact_role} at {brief.account_url}. "
            "Cover: who the account is and what they care about right now; who is in the room and what "
            "matters to them; where the seller's product fits; how it compares with competitors, if known; "
            "and three to five tailored talking points or questions to open with."
        )
