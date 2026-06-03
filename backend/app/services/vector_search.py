from sqlalchemy.orm import Session
from app.services.embeddings import embed_texts
from app.repositories.search_repo import search_similar_chunks

def search_chunks(db: Session, query: str, top_k: int, invoice_id: int | None = None):
    """
    Genera embedding de la query y busca top-k.
    """
    vectors = embed_texts([query])
    if not vectors:
        return []

    query_vector = vectors[0]
    rows = search_similar_chunks(db, query_vector, top_k, invoice_id)

    results = []
    for embedding, score in rows:
        results.append(
            {
                "invoice_id": embedding.invoice_id,
                "chunk_id": embedding.chunk_id,
                "content": embedding.content,
                "score": float(score),
                "start_index": (embedding.metadata_json or {}).get("start_index"),
            }
        )

    return results