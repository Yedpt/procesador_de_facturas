import json
from vertexai import init
from vertexai.generative_models import GenerativeModel, GenerationConfig
from app.config.settings import settings
from app.models.schemas import InvoiceExtracted


def extract_invoice_structured(text: str) -> dict:
    """
    Usa Gemini en Vertex AI para extraer un JSON estructurado de una factura.
    """
    init(project=settings.gcp_project_id, location=settings.gcp_location)
    model = GenerativeModel(settings.gemini_model)

    prompt = (
        "Extrae los campos de factura del siguiente texto. "
        "Devuelve SOLO JSON valido, sin comentarios ni markdown. "
        "Si un campo no aparece, usa null."
    )

    schema = InvoiceExtracted.model_json_schema()
    schema = _remove_nulls(schema)

    response = model.generate_content(
        [prompt, text],
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.1,
        ),
    )

    return json.loads(response.text)

def _remove_nulls(schema: dict) -> dict:
    if isinstance(schema, dict):
        if "anyOf" in schema:
            # quitar items que sean {"type": "null"}
            schema["anyOf"] = [
                s for s in schema["anyOf"]
                if not (isinstance(s, dict) and s.get("type") == "null")
            ]
            # si queda un solo schema, colapsa
            if len(schema["anyOf"]) == 1:
                schema.update(schema["anyOf"][0])
                del schema["anyOf"]

        for k, v in list(schema.items()):
            schema[k] = _remove_nulls(v)

    elif isinstance(schema, list):
        return [_remove_nulls(x) for x in schema]

    return schema