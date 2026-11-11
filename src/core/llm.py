"""Thin async wrapper around the Anthropic Messages API, shared by every agent."""

import os
from dataclasses import dataclass, field

import anthropic

DEFAULT_MODEL = "claude-sonnet-5-5"
# Server-side web search: Anthropic runs the searches and returns cited results.
# allowed_callers "direct" turns off dynamic filtering. With filtering on, Claude reads
# search results through code execution and the answer carries no web citations, and
# the source list is built from those citations.
WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search", "max_uses": 5, "allowed_callers": ["direct"]}
# The server-side search loop can pause a long turn; we resume it at most this many times.
MAX_CONTINUATIONS = 5


@dataclass(frozen=True)
class Source:
    title: str
    url: str


@dataclass
class AgentOutput:
    text: str
    # Pages cited in the text.
    sources: list[Source] = field(default_factory=list)
    # Every page the searches returned, cited or not.
    searched: list[Source] = field(default_factory=list)


class RefusalError(RuntimeError):
    """The model declined the request."""


class LLM:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model or os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)

    async def run(self, system: str, prompt: str, *, web_search: bool = False, effort: str = "medium") -> AgentOutput:
        """Runs one agent turn. With web_search, Claude searches the web and cites what it uses."""
        messages = [{"role": "user", "content": prompt}]
        options = {
            "model": self.model,
            "max_tokens": 16000,
            "system": system,
            "output_config": {"effort": effort},
            # If a safety classifier declines, the API retries on a fallback model in the same call.
            "betas": ["server-side-fallback-2026-07-01"],
            "fallbacks": "default",
        }
        if web_search:
            options["tools"] = [WEB_SEARCH_TOOL]

        content = []
        for _ in range(MAX_CONTINUATIONS + 1):
            response = await self.client.beta.messages.create(messages=messages, **options)
            if response.stop_reason == "refusal":
                category = response.stop_details.category if response.stop_details else None
                raise RefusalError(f"The model declined this request ({category or 'no category given'}).")
            content.extend(response.content)
            if response.stop_reason != "pause_turn":
                break
            # Resume a paused search loop by sending back everything produced so far.
            messages = [messages[0], {"role": "assistant", "content": content}]

        return AgentOutput(text=_text(content), sources=_sources(content), searched=_searched(content))


def _text(content) -> str:
    # Citations split the answer into several text blocks; joined, they read as one answer.
    return "".join(block.text for block in content if block.type == "text").strip()


def _sources(content) -> list[Source]:
    """The web pages Claude actually cited, in order of first use."""
    seen: dict[str, Source] = {}
    for block in content:
        if block.type != "text":
            continue
        for citation in block.citations or []:
            if citation.type == "web_search_result_location" and citation.url not in seen:
                seen[citation.url] = Source(title=citation.title or citation.url, url=citation.url)
    return list(seen.values())


def _searched(content) -> list[Source]:
    """Every page returned by web search in this turn, in order."""
    seen: dict[str, Source] = {}
    for block in content:
        if block.type != "web_search_tool_result" or not isinstance(block.content, list):
            continue  # an error result carries a single error object instead of a list
        for result in block.content:
            if result.url not in seen:
                seen[result.url] = Source(title=result.title or result.url, url=result.url)
    return list(seen.values())
