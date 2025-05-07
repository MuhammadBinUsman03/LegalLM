"""
API endpoints for the Legal Assistant service.
"""
import sys
import time
import uuid
import logging
from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from typing import Dict, Optional

# Add AI_core to path so we can import it
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the process_legal_request function from AI_core
from AI_core.main import process_legal_request

# Import models and config
from .models import QueryRequest, QueryResponse, HealthResponse
from ..config import API_PREFIX, API_VERSION, ALLOWED_ORIGINS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Legal Assistant API",
    description="API for interacting with the Legal AI Assistant",
    version=API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage to maintain context
# In production, use a persistent storage solution
sessions: Dict[str, Dict] = {}

@app.get(f"{API_PREFIX}/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running correctly.
    """
    return HealthResponse(
        status="ok",
        version=API_VERSION,
        components={
            "api": "healthy",
            "agent": "healthy",
            "tools": "healthy"
        }
    )

@app.post(f"{API_PREFIX}/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Process a legal query and return a response from the Legal AI Assistant.
    """
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Log request
    logger.info(f"Processing query for session {session_id}: {request.query[:50]}...")
    
    # Measure processing time
    start_time = time.time()
    
    try:
        # Process the query using the AI core
        response = await process_legal_request(request.query)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Return the response
        return QueryResponse(
            response=response,
            session_id=session_id,
            metadata={"tools_used": []},  # In a production version, track tools used
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your request: {str(e)}"
        )

@app.get(f"{API_PREFIX}/sessions/{{session_id}}")
async def get_session(session_id: str):
    """
    Get information about a specific session.
    """
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )
    
    return sessions[session_id]

@app.delete(f"{API_PREFIX}/sessions/{{session_id}}")
async def delete_session(session_id: str):
    """
    Delete a specific session.
    """
    if session_id in sessions:
        del sessions[session_id]
    
    return {"status": "success", "message": f"Session {session_id} deleted"}