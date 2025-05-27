"""Module that provides the configuration endpoint for the Survey Assist API.

This module contains the configuration endpoint for the Survey Assist API.
It defines the configuration endpoint and returns the current configuration settings.
"""

from fastapi import APIRouter, Depends

from soc_classification_vector_store.api.models.status_models import StatusResponse
from soc_classification_vector_store.utils.common import safe_int
from soc_classification_vector_store.utils.vector_store import vector_store_manager

router = APIRouter(tags=["Status"])

# Define the dependency at module level
vector_store_dependency = Depends(lambda : vector_store_manager)


@router.get("/status", response_model=StatusResponse)
async def get_status(vector_store=vector_store_dependency) -> StatusResponse:
    """Get the current status of the vector store.

    Args:
        vector_store: Vector store manager instance

    Returns:
        StatusResponse: A dictionary containing the current status.
    """
    status_resp = StatusResponse(
        status="ready" if vector_store.ready_event.is_set() else "loading",
        embedding_model_name=str(vector_store.status.get("embedding_model_name", "")),
        llm_model_name=str(vector_store.status.get("llm_model_name", "")),
        db_dir=str(vector_store.status.get("db_dir", "")),
        soc_index_file=str(vector_store.status.get("soc_index", "")),
        soc_structure_file=str(vector_store.status.get("soc_structure", "")),
        #soc_condensed_file=str(vector_store.status.get("soc_condensed", "")),
        matches=safe_int(vector_store.status.get("matches", 0)),
        index_size=safe_int(vector_store.status.get("index_size", 0)),
    )
    return status_resp
