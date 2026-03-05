from fastapi import APIRouter, Depends
from qdrant_client import QdrantClient

from app.config import settings
from app.dependencies.auth import verify_api_key

router = APIRouter()


@router.get("/stats")
def stats(_=Depends(verify_api_key)):
    client = QdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
    )

    collection_info = client.get_collection(settings.collection_name)

    # Obtener todos los puntos (chunks) con payload
    points, _ = client.scroll(
        collection_name=settings.collection_name,
        limit=1000,  # suficiente para esta prueba
        with_payload=True,
    )

    filenames = set()
    last_ingest = None

    for point in points:
        payload = point.payload or {}

        filename = payload.get("filename")
        ingest_ts = payload.get("ingest_timestamp")

        if filename:
            filenames.add(filename)

        if ingest_ts:
            if not last_ingest or ingest_ts > last_ingest:
                last_ingest = ingest_ts

    return {
        "collection_name": settings.collection_name,
        "documents_count": len(filenames),
        "chunks_count": collection_info.points_count,
        "last_ingest": last_ingest,
        "status": collection_info.status,
    }