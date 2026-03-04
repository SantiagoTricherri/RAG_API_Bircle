from pydantic import BaseModel
from typing import Optional, Dict


class QueryRequest(BaseModel):
    q: str
    top_k: Optional[int] = 5
    filters: Optional[Dict[str, str]] = None