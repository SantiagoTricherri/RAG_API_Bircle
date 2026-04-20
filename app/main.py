from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, ingest, query, stats, upload
from app.middleware.logging_middleware import log_requests

app = FastAPI(title="RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(stats.router)
app.include_router(upload.router)