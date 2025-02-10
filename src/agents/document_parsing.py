from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.agents.base import Agent
from src.core.llm import LLM


class DocumentParsingAgent(Agent):
    def __init__(self, file: UploadedFile):
        super().__init__("DocumentParsingAgent")
        self.file = file

    async def generate(self, llm: LLM, **kwargs) -> str:
        parsed_text = llm.extract_text_from_file(self.file)
        print(parsed_text)
        prompt = (
            f"Based on the following product overview content:\n{parsed_text}\n"
            "Extract additional insights into the product's value proposition and key selling points."
        )
        return await llm.generate_insight_async(prompt)