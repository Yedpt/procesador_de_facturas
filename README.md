# Procesador de Facturas (Invoice Intelligence Platform)

[![Backend](https://img.shields.io/badge/backend-FastAPI-009688?style=flat-square)](backend/)
[![DB](https://img.shields.io/badge/database-PostgreSQL-336791?style=flat-square)](https://www.postgresql.org/)
[![OCR](https://img.shields.io/badge/OCR-Tesseract-2E7D32?style=flat-square)](https://github.com/tesseract-ocr/tesseract)
[![LLM](https://img.shields.io/badge/LLM-Gemini%20Vertex-1E88E5?style=flat-square)](https://cloud.google.com/vertex-ai)

Proyecto personal para construir un pipeline de IA documental end-to-end con RAG y un copilot conversacional. El objetivo es procesar facturas desde PDF, extraer datos estructurados, validar coherencia, persistir con trazabilidad y habilitar busqueda semantica y chat.

---

## Que hace este proyecto

- Ingesta de PDFs (nativos y escaneados).
- OCR para documentos escaneados.
- Extraccion estructurada a JSON con Vertex AI (Gemini).
- Validacion de negocio (subtotal, IVA, retencion, total).
- Persistencia y trazabilidad de cada paso del pipeline.
- Proxima fase: RAG sobre facturas (busqueda semantica y Q&A).

---

## Stack tecnico

- Backend: FastAPI, Pydantic, SQLAlchemy
- DB: PostgreSQL
- OCR: PyMuPDF (fitz), pytesseract, Pillow
- LLM: Gemini en Vertex AI
- Vector DB (fase 2): pgvector

---

## Estado del roadmap

| Fase | Estado | Descripcion |
|------|--------|-------------|
| Fase 1 - MVP pipeline documental | DONE | Ingesta PDF, OCR, extraccion estructurada, validacion, persistencia, trazabilidad |
| Fase 2 - RAG sobre documentos | IN PROGRESS | Chunking, embeddings, pgvector, search y ask |
| Fase 3 - Agente conversacional | PLANNED | Tools, memoria, PII masking (Presidio), LangGraph |
| Fase 4 - Produccion enterprise | PLANNED | RAGAS, LangSmith, busqueda hibrida, tests de regresion |
| Fase 5 - Frontend (React) | PLANNED | UI para upload, busqueda y chat |
| Fase 6 - Cierre del producto | PLANNED | Demo final, docs, despliegue |

---

## Fase 1 (completada)

Incluye el pipeline base:

- Deteccion de PDF escaneado vs nativo.
- OCR con Tesseract.
- Extraccion estructurada en JSON con Gemini (Vertex AI).
- Validacion de totales y coherencia.
- Persistencia y trazabilidad del pipeline.

Endpoints principales:

- `POST /invoices/detect-scanned`
- `POST /invoices/extract-text`
- `POST /invoices/extract-structured`

---

## Fase 2 (en progreso)

Objetivo: habilitar RAG y preguntas semanticas sobre facturas procesadas.

- Chunking del texto
- Embeddings
- Almacenamiento en pgvector
- Endpoints: `/search` y `/ask`

---

## Como ejecutar (Docker)

Requisitos:
- Docker Desktop
- Archivo de credenciales GCP (service account) en `backend/secrets/gcp-sa.json`

Comandos:

```bash
./manage.sh backend
```

Salud:

```
GET http://localhost:8000/health
```

---

## Estructura general

```
backend/
  app/
    config/
    controllers/
    models/
    repositories/
    services/
    pipelines/
```

---

## Notas

- El archivo `backend/.env` define las variables para Vertex AI.
- Si cambias dependencias, ejecuta `./manage.sh rebuild`.

---

## Licencia

Consulta el archivo [LICENSE](LICENSE).
