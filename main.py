from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config.config_parser import settings
from src.logging.logger import logger
from src.core.factories import ModelFactory

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"=== Starting {settings.app_name} v{settings.app_version} ===")
    logger.info("Warming up model (Singleton via ModelFactory)...")
    ModelFactory.get_model()
    yield
    logger.info("=== Shutting down application ===")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

@app.get("/", tags=["Health Check"])
def health_check():
    logger.info("Health check endpoint was hit.")
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)