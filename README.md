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