from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.repositories.invoice_repo import create_invoice, update_invoice_data
from app.repositories.trace_repo import add_trace
from app.models.schemas import InvoiceOut, InvoiceValidationOut

from app.services.pdf_ingest import detect_scanned_pdf, extract_text_from_pdf
from app.models.schemas import PdfScanCheckOut
from app.services.pdf_ingest import extract_text_from_pdf
from app.models.schemas import PdfTextOut
from app.services.extractor import extract_invoice_structured
from app.services.validator import validate_invoice_totals


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

@router.post("/extract-structured")
async def extract_structured(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 1) Crear invoice base
    invoice = create_invoice(db, file.filename)
    add_trace(db, invoice.id, "ingest", "ok")

    # 2) Extraer texto
    pdf_bytes = await file.read()
    text_result = extract_text_from_pdf(pdf_bytes)
    add_trace(db, invoice.id, "extract_text", "ok", f"source={text_result['source']}")

    # 3) Extraer JSON con Gemini
    structured = extract_invoice_structured(text_result["text"])
    add_trace(db, invoice.id, "extract_structured", "ok")

    # 4) Validar negocio
    validation = validate_invoice_totals(structured)
    add_trace(db, invoice.id, "validate", "ok", f"is_valid={validation['is_valid']}")

    # 5) Persistir todo
    updated = update_invoice_data(
        db=db,
        invoice_id=invoice.id,
        source=text_result["source"],
        is_scanned=text_result["is_scanned"],
        raw_text=text_result["text"],
        extracted_data=structured,
        validation=validation,
        status="processed",
    )
    add_trace(db, invoice.id, "persist", "ok")

    return {
        "invoice_id": updated.id,
        "source": updated.source,
        "is_scanned": updated.is_scanned,
        "data": updated.extracted_data,
        "validation": updated.validation,
    }


