from google import genai
from PyPDF2 import PdfReader

class LLM:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)

    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """Extract text from a PDF file (extend this for DOCX, etc.)."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            return f"Error parsing file: {e}"

