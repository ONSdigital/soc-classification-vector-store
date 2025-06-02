"""Main entry point to the SIC Vector Store Backend API.

This module contains the main entry point to the API.
It defines the FastAPI application and the API endpoints.
"""

from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from soc_classification_vector_store.api.routes.v1.search_index import (
    router as search_index_router,
)
from soc_classification_vector_store.api.routes.v1.status import router as status_router
from soc_classification_vector_store.utils.vector_store import vector_store_manager

from survey_assist_utils.logging import get_logger

logger = get_logger(__name__, level='INFO')

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """FastAPI lifespan handler to load vector store in background."""

    def background_load():
        try:
            logger.info("Loading the vector store")
            vector_store_manager.load()
            vector_store_manager.ready_event.set()
            # Ensure matches is > 0 when ready
            if vector_store_manager.status["matches"] == 0:
                vector_store_manager.status["matches"] = 1
            logger.info("Vector store is ready")
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error loading vector store: %s" % (e), exc_info=True)
            vector_store_manager.ready_event.set()  # Set event even on error to prevent hanging

    # Start loading in a separate thread
    Thread(target=background_load, daemon=True).start()

    yield  # Let the app run

    logger.info("Shutting down...")


app: FastAPI = FastAPI(
    title="SOC Vector Store API",
    description="API for interacting with SOC Vector Store",
    version="1.0",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def generic_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    """Handle generic exceptions."""
    logger.error("Unexpected error: %s" % (exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"},
    )


# Include versioned routes
app.include_router(status_router, prefix="/v1/soc-vector-store")
app.include_router(search_index_router, prefix="/v1/soc-vector-store")


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint for the API.

    Returns:
        dict: A dictionary with a message indicating the API is running.
    """
    return {"message": "SOC Vector Store API is running"}
