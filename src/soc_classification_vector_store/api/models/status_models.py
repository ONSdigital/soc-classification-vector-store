"""This module contains the models for the status response.

The models in this module are used to represent the response
returned by the API.
"""

from pydantic import BaseModel


class StatusResponse(BaseModel):
    """Model representing the vector store status response.

    Attributes:
        embedding_model_name (str): The name of the embeddings model.
        matches (int): The number of nearest matches initialised in the vector store.
        status (str): The status of the vector store.
    """

    status: str
    embedding_model_name: str
    llm_model_name: str
    db_dir: str
    soc_index_file: str
    soc_structure_file: str
    # soc_condensed_file: str
    matches: int
    index_size: int
