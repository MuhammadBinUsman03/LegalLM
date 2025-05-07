"""
Server script to run the FastAPI application for the Legal Assistant API.
"""
import uvicorn
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Import configuration
from ..config import HOST, PORT, DEBUG

# Configure logging
logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_server():
    """
    Run the FastAPI server with uvicorn.
    """
    logger.info(f"Starting Legal Assistant API server at http://{HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    
    uvicorn.run(
        "backend.endpoint.api:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info" if not DEBUG else "debug"
    )

if __name__ == "__main__":
    run_server()