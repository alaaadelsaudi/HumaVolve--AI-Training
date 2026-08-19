from fastapi import APIRouter, HTTPException, status, UploadFile, File
from src.models.schemas import IngestResponse
from src.services.ingest_service import IngestionService
from src.logging.logger import logger
from src.config.config_parser import settings

router = APIRouter(prefix="/api/v1", tags=["Ingestion"])
ingest_service = IngestionService()

@router.post("/ingest", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def upload_and_ingest(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(('.txt', '.md', '.csv')):
            raise HTTPException(status_code=400, detail="Only .txt, .md, .csv files are supported.")
        chunks_count = await ingest_service.process_uploaded_file(
            file, chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
        )
        return IngestResponse(
            message=f"File '{file.filename}' indexed successfully.",
            chunks_indexed=chunks_count,
            index_path=settings.vector_index_path
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ingestion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))