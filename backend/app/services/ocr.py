import io
import fitz # PyMuPDF
from PIL import Image
import pytesseract


def ocr_pdf_pages(pdf_bytes: bytes, dpi: int = 300) -> str:
    """
    Convierte cada pagina del PDF a imagen y aplica OCR.
    Devuelve todo el texto concatenado.
    """ 

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    texts = []

    for page in doc:
        # Renderizar la página a una imagen
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))

        page_text = pytesseract.image_to_string(img)
        texts.append(page_text)
    
    return "\n".join(texts)