from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.repositories.invoice_repo import create_invoice
from app.models.schemas import InvoiceOut

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/process", response_model=InvoiceOut)
def process_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # MVP: guardar metadata basica y devolverla
    invoice = create_invoice(db, file.filename)
    return invoice