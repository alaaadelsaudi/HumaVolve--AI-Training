from fastapi import APIRouter, HTTPException, status
from src.models.schemas import QueryRequest, QueryResponse
from src.services.rag_service import RAGService
from src.logging.logger import logger

router = APIRouter(prefix="/api/v1", tags=["RAG Queries"])
rag_service = RAGService()

@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
def process_query(request: QueryRequest):
    try:
        if not request.ticket.strip():
            raise HTTPException(status_code=400, detail="Ticket cannot be empty.")
        result = rag_service.answer_ticket(request.ticket)
        return QueryResponse(**result)
    except HTTPException:
        raise
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No FAISS index found. Call /api/v1/ingest first.")
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))