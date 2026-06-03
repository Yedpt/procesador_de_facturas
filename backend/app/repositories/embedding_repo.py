from sqlalchemy.orm import Session
from app.models.entities import InvoiceEmbedding

def save_embeddings(
    db: Session,
    invoice_id: int,
    items: list[dict],
) -> int:
    """
    Guarda una lista de embeddings en la tabla invoice_embeddings.
    """
    for item in items:
        db.add(
            InvoiceEmbedding(
                invoice_id=invoice_id,
                chunk_id=item["chunk_id"],
                content=item["content"],
                embedding=item["embedding"],
                metadata_json=item.get("metadata_json"),
            )
        )

    db.commit()
    return len(items)