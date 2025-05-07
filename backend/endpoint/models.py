"""
Pydantic models for the API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class QueryRequest(BaseModel):
    """Model for legal query requests."""
    query: str = Field(..., description="The legal query or request from the user")
    session_id: Optional[str] = Field(None, description="Session identifier for tracking conversation context")
    options: Optional[Dict[str, Any]] = Field(None, description="Additional options for query processing")


class QueryResponse(BaseModel):
    """Model for legal query responses."""
    response: str = Field(..., description="The response from the legal assistant")
    session_id: Optional[str] = Field(None, description="Session identifier that tracks the conversation")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the response")
    processing_time: Optional[float] = Field(None, description="Time taken to process the query in seconds")


class HealthResponse(BaseModel):
    """Model for health check responses."""
    status: str = Field(..., description="Health status of the API")
    version: str = Field(..., description="API version")
    components: Dict[str, str] = Field(..., description="Status of individual components")