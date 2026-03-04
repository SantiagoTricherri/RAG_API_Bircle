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

    return {
        "collection_name": settings.collection_name,
        "points_count": collection_info.points_count,
        "status": collection_info.status,
    }