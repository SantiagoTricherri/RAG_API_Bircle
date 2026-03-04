from pydantic import BaseModel
from typing import List, Dict, Any


class SourceItem(BaseModel):
    doc_id: str
    filename: str | None = None
    score: float
    snippet: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    retrieval_params: Dict[str, Any]