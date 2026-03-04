# RAG API – FastAPI + LlamaIndex + Qdrant

API REST que implementa un sistema RAG (Retrieval-Augmented Generation) con persistencia de embeddings y vector store en Qdrant.

## Arquitectura

- FastAPI (API layer)
- LlamaIndex (RAG orchestration)
- OpenAI (LLM + Embeddings)
- Qdrant (Vector Store persistente)
- Docker (Qdrant)
- Pytest (tests automatizados)

Flujo:

1. Ingesta de documentos (.txt, .pdf)
2. Chunking + embeddings
3. Persistencia en Qdrant
4. Query RAG con fuentes citadas

## Setup local

### 1. Clonar repositorio

(bash)
git clone ...
cd rag-api

### 2. Crear entorno virtual

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Configurar variables de entorno

OPENAI_API_KEY=key (supersecret)

### 4. Levantar Qdrant

docker compose up -d

### 5. Ejecutar API

uvicorn app.main:app --reload


---

### Uso

## Endpoints

### GET /health
Estado del servicio.

### POST /ingest
Ingesta de documentos desde carpeta `/data`.

Requiere header:
X-API-Key: supersecret

### POST /query
Consulta RAG.

Body ejemplo:
{
  "q": "¿Qué es LlamaIndex?",
  "top_k": 5
}

Devuelve:
- answer
- sources (con score y snippet)
- retrieval_params

### GET /stats
Información del vector store.

---

### Tests

## Tests

Ejecutar:

(bash)
pytest


---

### Decisiones técnicas


## Decisiones técnicas

- Se implementó threshold mínimo de similitud para evitar respuestas irrelevantes.
- Se definió un system prompt restrictivo para reducir alucinaciones.
- Persistencia real en Qdrant (no reconstrucción en cada arranque).
- Separación en capas: routers, services, models, dependencies.
- Seguridad mínima por API key.


## Posibles mejoras

- Filtros avanzados por metadata
- Deduplicación por hash de archivo
- Streaming SSE
- Rate limiting
- Observabilidad (Prometheus)
- Multi-tenant collections

