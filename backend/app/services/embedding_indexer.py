from sqlalchemy.orm import Session
from app.services.chunking import split_text_into_chunks
from app.services.embeddings import embed_texts
from app.repositories.embedding_repo import save_embeddings

def index_invoice_embeddings(db: Session, invoice_id: int, raw_text: str) -> int:
    """
    Parte el texto en chunks, genera embeddings y los guarda.
    """
    chunks = split_text_into_chunks(raw_text)
    texts = [c["content"] for c in chunks]

    vectors = embed_texts(texts)

    payload = []
    for chunk, vector in zip(chunks, vectors):
        payload.append(
            {
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "embedding": vector,
                "metadata_json": {
                    "start_index": chunk.get("start_index"),
                },
            }
        )

    return save_embeddings(db, invoice_id, payload)