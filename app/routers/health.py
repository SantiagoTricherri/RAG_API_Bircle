from fastapi import APIRouter
from app.services.vector_store import get_index

router = APIRouter()


@router.get("/health")
def health():
    try:
        index = get_index()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}