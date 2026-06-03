from vertexai import init
from vertexai.generative_models import GenerativeModel, GenerationConfig
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.services.vector_search import search_chunks

def answer_question(db: Session, query: str, top_k: int, invoice_id: int | None = None) -> dict:
    """
    Genera una respuesta basada en los chunks mas similares.
    - Usa RAG: primero recupera top-k chunks y luego responde con Gemini.
    - Devuelve respuesta final y los chunks usados.
    """
    results = search_chunks(db, query, top_k, invoice_id)

    context = "\n\n".join(
        [f"[{r['chunk_id']}] {r['content']}" for r in results]
    )

    prompt = (
        "Responde la pregunta usando SOLO el contexto. "
        "Si no hay informacion suficiente, di claramente que no se encontro evidencia.\n\n"
        f"Pregunta: {query}\n\n"
        f"Contexto:\n{context}"
    )

    init(project=settings.gcp_project_id, location=settings.gcp_location)
    model = GenerativeModel(settings.gemini_model)

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=0.2,
        ),
    )

    return {
        "answer": response.text,
        "used_chunks": results,
    }