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