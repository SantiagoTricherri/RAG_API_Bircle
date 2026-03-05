# RAG API – FastAPI + LlamaIndex + Qdrant

API REST que implementa un sistema RAG con persistencia de embeddings y vector store en Qdrant.

El sistema permite:

- Ingestar documentos .txt y .pdf

- Consultarlos vía RAG

- Controlar alucinaciones

- Obtener métricas operativas

- Contar con logging estructurado

## Arquitectura

- FastAPI (API layer)
- LlamaIndex (RAG orchestration)
- OpenAI (LLM + Embeddings)
- Qdrant (Vector Store persistente)
- Docker (Qdrant)
- Pytest (tests automatizados)
- Middleware personalizado – Logging estructurado con request_id

Flujo:

1. Ingesta de documentos (.txt, .pdf)
2. Chunking configurable (SentenceSplitter)
3. Generación de embeddings
4. Persistencia en Qdrant
5. Retrieval por similitud
6. Generación de respuesta con control de alucinación
7. Devolución de fuentes citadas

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

OPENAI_API_KEY=openai_key
API_KEY=supersecret
QDRANT_HOST=localhost
QDRANT_PORT=6333
COLLECTION_NAME=documents

### 4. Levantar Qdrant

docker compose up -d

### 5. Ejecutar API

uvicorn app.main:app --reload


---


# USO

## Autenticación

Los endpoints protegidos requieren:

X-API-Key: supersecret

## Endpoints

### GET /health
Estado del servicio.

### POST /ingest
Ingesta de documentos desde carpeta `/data`.

Requiere header:
X-API-Key: supersecret

### POST /upload

Permite subir archivos .txt o .pdf vía multipart/form-data.
- Guarda el archivo en /data
- Extrae contenido
- Genera embeddings
- Persiste en Qdrant

### POST /query
Consulta RAG.

Body ejemplo:
{
  "q": "¿Qué es LlamaIndex?",
  "top_k": 5
}

Devuelve:
{
  "answer": "...",
  "sources": [
    {
      "doc_id": "...",
      "filename": "file.txt",
      "score": 0.72,
      "snippet": "..."
    }
  ],
  "retrieval_params": {
    "top_k": 5
  }
}

#### Control de Alucinación

- Se aplica threshold mínimo de similitud
- Se aplica verificación de score máximo
- Prompt restrictivo obliga a usar solo contexto recuperado
- Si no hay contexto relevante → respuesta explícita controlada

### GET /stats
Devuelve métricas reales del vector store:

{
  "collection_name": "documents",
  "documents_count": 3,
  "chunks_count": 12,
  "last_ingest": "2026-03-04T20:24:09",
  "status": "green"
}

Incluye:
- Documentos únicos
- Cantidad de chunks
- Última ingesta
- Estado de la colección

### Logging estructurado

Se implementa middleware HTTP que genera logs JSON con:
- request_id
- method
- path
- status_code
- duration

Ejemplo:
{
  "level": "INFO",
  "request_id": "uuid",
  "method": "POST",
  "path": "/query",
  "status_code": 200,
  "duration": 0.84
}


---


## Tests

Ejecutar:

(bash)
pytest

Incluye tests para:
- Health endpoint
- Autenticación
- Query estructural


---


## Decisiones técnicas

- Persistencia real en Qdrant (no reindexa al reiniciar)
- Chunking controlado con SentenceSplitter
- Metadata enriquecida por documento:
  - filename
  - mime_type
  - size
  - ingest_timestamp
- Threshold tuning para reducir falsos positivos
- Score gating adicional para evitar similitud estructural engañosa
- Prompt hardening para minimizar alucinaciones
- Arquitectura modular:
  - routers
  - services
  - dependencies
  - middleware
  - models
- Configuración vía variables de entorno
