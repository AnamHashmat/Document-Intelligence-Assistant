"""Extract text from uploaded PDF files. Implementation comes in the next stage."""

import fitz  # PyMuPDF


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Return text extracted from all pages of a PDF."""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        return "\n".join(page.get_text("text") for page in document)
