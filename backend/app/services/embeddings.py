from vertexai import init
from vertexai.language_models import TextEmbeddingModel
from app.config.settings import settings

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Usa el modelo de embeddings de Vertex AI para convertir una lista de textos en vectores numéricos.
    """
    if not texts:
        return []
    
    init(project=settings.gcp_project_id, location=settings.gcp_location)
    model = TextEmbeddingModel.from_pretrained(settings.embeddings_model)

    embeddings = model.get_embeddings(texts)
    return [e.values for e in embeddings]