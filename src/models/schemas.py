from pydantic import BaseModel, Field
from typing import Optional

class QueryRequest(BaseModel):
    ticket: str = Field(..., description="Customer problem description", example="النت فاصل عندي")

class QueryResponse(BaseModel):
    ticket: str
    response: str
    sources_count: int = Field(..., ge=0)
    execution_time_seconds: float
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class IngestRequest(BaseModel):
    file_path: Optional[str] = None

class IngestResponse(BaseModel):
    message: str
    chunks_indexed: int = Field(..., ge=0)
    index_path: str