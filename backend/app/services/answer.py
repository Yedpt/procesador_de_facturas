from vertexai import init
from vertexai.generative_models import GenerativeModel, GenerationConfig
from app.config.settings import settings
from app.services.vector_search import search_chunks

def answer_question(query: str, top_k: int, invoice_id: int | None = None) -> dict:
    """
    Construye una respuesta en lenguaje natural usando RAG.
    Pasos:
    1) Busca los top-k chunks mas similares a la pregunta.
    2) Construye un contexto compacto con esos chunks.
    3) Llama a Gemini para responder solo con esa evidencia.
    4) Devuelve la respuesta y los chunks usados.
    """
    # 1) Buscar contexto relevante
    results = search_chunks(db=None, query=query, top_k=top_k, invoice_id=invoice_id)
    # Nota: este servicio no accede a DB directamente; la busqueda real se hace en el endpoint con db.
    # Aqui dejamos la estructura para el wrapper en el endpoint (ver paso 3).

    return {"answer": "", "used_chunks": results}