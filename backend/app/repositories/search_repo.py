from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.entities import InvoiceEmbedding

def search_similar_chunks(
    db: Session,
    query_vector: list[float],
    top_k: int,
    invoice_id: int | None = None,
) -> list[tuple[InvoiceEmbedding, float]]:
    """
    Busca los chunks mas similares usando distancia L2.
    Devuelve tuplas (InvoiceEmbedding, score).
    """
    distance = InvoiceEmbedding.embedding.l2_distance(query_vector).label("score")

    stmt = select(InvoiceEmbedding, distance)
    if invoice_id is not None:
        stmt = stmt.where(InvoiceEmbedding.invoice_id == invoice_id)

    stmt = stmt.order_by(distance).limit(top_k)
    return db.execute(stmt).all()