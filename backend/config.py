"""
Backend configuration settings.
"""
import os

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# API configuration
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# CORS settings
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "*"  # For development - remove in production
]

# Rate limiting
RATE_LIMIT = "100/minute"