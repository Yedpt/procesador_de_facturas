import fitz  # PyMuPDF
from app.services.ocr import ocr_pdf_pages

def detect_scanned_pdf(pdf_bytes: bytes, min_text_chars: int = 50) -> dict:
    """
    Detecta si un PDF es escaneado usando una heuristica simple:
    - Si el texto total es muy bajo, asumimos que es escaneado.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    total_text_chars = 0
    for page in doc:
        page_text = page.get_text("text")
        total_text_chars += len(page_text.strip())

    is_scanned = total_text_chars < min_text_chars

    return {
        "is_scanned": is_scanned,
        "total_text_chars": total_text_chars,
        "page_count": doc.page_count,
    }


def extract_text_from_pdf(pdf_bytes: bytes, min_text_chars: int = 50) -> dict:
    """
    Extrae texto de PDF nativo si hay texto suficiente.
    Si es escaneado, usa OCR.
    """

    scan_info = detect_scanned_pdf(pdf_bytes, min_text_chars=min_text_chars)

    if scan_info["is_scanned"]:
        text = ocr_pdf_pages(pdf_bytes)
        source = "ocr"
    else:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc)
        source = "native"

    return {
        "text": text,
        "source": source,
        **scan_info,
    }