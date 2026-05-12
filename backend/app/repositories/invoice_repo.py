from sqlalchemy.orm import Session
from app.models.entities import Invoice


def create_invoice(db: Session, file_name: str) -> Invoice:
    invoice = Invoice(file_name=file_name, status="pending")
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def get_invoice(db: Session, invoice_id: int) -> Invoice | None:
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def update_invoice_data(
    db: Session,
    invoice_id: int,
    source: str,
    is_scanned: bool,
    raw_text: str,
    extracted_data: dict,
    validation: dict,
    status: str = "processed",
):
    invoice = get_invoice(db, invoice_id)
    if not invoice:
        return None

    invoice.source = source
    invoice.is_scanned = is_scanned
    invoice.raw_text = raw_text
    invoice.extracted_data = extracted_data
    invoice.validation = validation
    invoice.status = status

    db.commit()
    db.refresh(invoice)
    return invoice