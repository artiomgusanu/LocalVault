import pymupdf

from localvault.domain.errors import ExtractionError

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = pymupdf.open(pdf_path)
    try:
        if doc.needs_pass:
            raise ExtractionError(f"Encrypted PDF, cannot read: {pdf_path}")

        pages_text = [page.get_text() for page in doc]
    finally:
        doc.close()

    text = "\n".join(pages_text).strip()

    if not text:
        raise ExtractionError(f"No extractable text (scanned image?): {pdf_path}")

    return text