"""Plain-text extraction from an uploaded product document (PDF, DOCX, PPTX or TXT)."""

import os
from typing import BinaryIO

import docx
from pptx import Presentation
from pypdf import PdfReader

SUPPORTED = (".pdf", ".docx", ".pptx", ".txt")


def extract_text(file: BinaryIO, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    file.seek(0)
    if ext == ".txt":
        return file.read().decode("utf-8", errors="replace")
    if ext == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(file).pages)
    if ext == ".docx":
        return "\n".join(p.text for p in docx.Document(file).paragraphs if p.text)
    if ext == ".pptx":
        return "\n".join(
            shape.text
            for slide in Presentation(file).slides
            for shape in slide.shapes
            if getattr(shape, "text", "")
        )
    raise ValueError(f"Unsupported file type {ext or '(none)'}. Use one of: {', '.join(SUPPORTED)}.")
