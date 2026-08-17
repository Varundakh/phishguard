#!/usr/bin/env python3
# PhishGuard - Application Entry Point
# Run this file to start the server

import uvicorn
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
