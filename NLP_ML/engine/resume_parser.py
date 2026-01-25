# NLP_ML/engine/resume_parser.py

from __future__ import annotations
import os
from typing import Optional

import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF resume using pdfplumber."""
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(page_text.strip())
    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX resume using python-docx."""
    doc = Document(file_path)
    text_parts = []
    for para in doc.paragraphs:
        if para.text and para.text.strip():
            text_parts.append(para.text.strip())
    return "\n".join(text_parts).strip()


def extract_text(file_path: str) -> str:
    """
    Auto-detect file type (PDF/DOCX/TXT) and extract text.
    Returns extracted text. If text is not found, returns empty string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    if ext == ".docx":
        return extract_text_from_docx(file_path)

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()

    raise ValueError(f"Unsupported resume format: {ext}. Use .pdf, .docx, or .txt")
