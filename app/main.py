# PhishGuard - Main FastAPI Application
# Application entry point and configuration

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from app.core.config import get_settings
from app.core.logging_config import logger
from app.database.database import init_db
from app.api.routes import router as api_router
from app.api.middleware import SecurityHeadersMiddleware, LoggingMiddleware, CORSMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    logger.info("Starting PhishGuard application")
    init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down PhishGuard application")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware)

# Include API routes
app.include_router(api_router)

# Mount static files (frontend)
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def root():
    """
    Serve the main dashboard
    """
    if os.path.exists("frontend/index.html"):
        return FileResponse("frontend/index.html")
    return {"message": "PhishGuard API - Intelligent Phishing URL Analyzer"}


@app.get("/dashboard")
async def dashboard():
    """
    Serve the dashboard page
    """
    if os.path.exists("frontend/dashboard.html"):
        return FileResponse("frontend/dashboard.html")
    return {"message": "Dashboard - Coming Soon"}


@app.get("/history")
async def history():
    """
    Serve the scan history page
    """
    if os.path.exists("frontend/history.html"):
        return FileResponse("frontend/history.html")
    return {"message": "History - Coming Soon"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
