from pydantic import BaseModel
from typing import List, Dict, Any

class IngestResponse(BaseModel):
    document_id: str
    filename: str
    message: str

class QueryRequest(BaseModel):
    query: str
    limit: int = 5
    filters: Dict[str, Any] = None

class Source(BaseModel):
    id: str
    content: str
    similarity: float
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
