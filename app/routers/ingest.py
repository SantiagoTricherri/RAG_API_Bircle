from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.auth import verify_api_key
from app.services.ingest_service import ingest_directory

router = APIRouter()


@router.post("/ingest")
def ingest(
    _=Depends(verify_api_key)
):
    try:
        result = ingest_directory()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))