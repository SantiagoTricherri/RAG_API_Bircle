from fastapi import FastAPI
from app.routers import health, ingest, query, stats

app = FastAPI(title="RAG API")

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(stats.router)