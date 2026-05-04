from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.repositories.invoice_repo import create_invoice
from app.models.schemas import InvoiceOut

from app.services.pdf_ingest import detect_scanned_pdf
from app.models.schemas import PdfScanCheckOut
from app.services.pdf_ingest import extract_text_from_pdf
from app.models.schemas import PdfTextOut

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/process", response_model=InvoiceOut)
def process_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # MVP: guardar metadata basica y devolverla
    invoice = create_invoice(db, file.filename)
    return invoice

@router.post("/detect-scanned", response_model=PdfScanCheckOut)
async def detect_scanned(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    result = detect_scanned_pdf(pdf_bytes)
    return result

@router.post("/extract-text", response_model=PdfTextOut)
async def extract_text(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    result = extract_text_from_pdf(pdf_bytes)
    return result