from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.auth import verify_api_key
from app.models.request_models import QueryRequest
from app.services.rag_service import query_rag

router = APIRouter()


@router.post("/query")
def query_endpoint(
    request: QueryRequest,
    _=Depends(verify_api_key)
):
    try:
        result = query_rag(
            question=request.q,
            top_k=request.top_k,
        )

        # Si no hay sources relevantes
        if not result["sources"]:
            return {
                "answer": "No relevant context found to answer the question.",
                "sources": [],
                "retrieval_params": {"top_k": request.top_k},
            }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))