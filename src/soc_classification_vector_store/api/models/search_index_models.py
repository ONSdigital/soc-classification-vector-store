"""This module contains the models for the status response.

The models in this module are used to represent the response
returned by the API.
"""

from pydantic import BaseModel


class SearchIndexRequest(BaseModel):
    """Model representing a request to the vector store search index."""
    #TODO: check what fields are required for SOC
    industry_descr: str
    job_title: str
    job_description: str


class SearchIndexItem(BaseModel):
    """Model representing an item in the vector store search index.

    Attributes:
        distance (float): vector search distance.
        title (str): soc title description.
        code (str): soc code.
        four_digit_code (str): four digit soc code.
        two_digit_code (str): two digit soc code.
    """

    distance: float
    title: str
    code: str
    four_digit_code: str
    two_digit_code: str


class SearchIndexResponse(BaseModel):
    """Model representing the vector store search index multi response."""

    results: list[SearchIndexItem]
