from fastapi import FastAPI
from app.routers import health, ingest, query, stats, upload
from app.middleware.logging_middleware import log_requests

app = FastAPI(title="RAG API")
app.middleware("http")(log_requests)

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(stats.router)
app.include_router(upload.router)