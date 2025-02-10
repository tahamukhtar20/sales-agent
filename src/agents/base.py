from abc import ABC, abstractmethod

from src.core.llm import LLM


class Agent(ABC):
    """Abstract base class for specialized agents."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def generate(self, llm: LLM, **kwargs) -> str:
        """Generate insights using the provided LLM instance."""
        pass