from sqlalchemy.orm import Session
from app.models.entities import InvoiceTrace


def add_trace(db: Session, invoice_id: int, step: str, status: str, message: str | None = None):
    trace = InvoiceTrace(
        invoice_id=invoice_id,
        step=step,
        status=status,
        message=message,
    )
    db.add(trace)
    db.commit()
    db.refresh(trace)
    return trace