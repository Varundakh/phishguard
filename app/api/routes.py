# PhishGuard - API Routes
# FastAPI endpoint definitions

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.database import get_db
from app.schemas.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ScansList,
    Statistics,
    HealthResponse,
    ErrorResponse
)
from app.services.analyzer import URLAnalyzerService
from app.services.database import DatabaseService
from app.services.statistics import StatisticsService
from app.core.config import get_settings
from app.core.logging_config import logger

# Create router
router = APIRouter(prefix="/api", tags=["phishguard"])

settings = get_settings()


@router.post("/analyze", response_model=AnalyzeResponse, status_code=200)
async def analyze_url(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze URL for phishing risk
    
    **Endpoint:** `POST /api/analyze`
    
    **Request Body:**
    ```json
    {
        "url": "https://example.com/login"
    }
    ```
    
    **Response:**
    ```json
    {
        "scan_id": "550e8400-e29b-41d4-a716-446655440000",
        "url": "https://example.com/login",
        "risk_score": 42,
        "risk_level": "MODERATE",
        "indicators": [...],
        "scoring_breakdown": [...],
        "recommendations": "...",
        "technical_details": {...},
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    
    **Status Codes:**
    - `200`: Successful analysis
    - `400`: Invalid URL format
    - `500`: Internal server error
    """
    try:
        logger.info(f"Analyzing URL: {request.url}")
        
        # Analyze URL
        result = URLAnalyzerService.analyze_url(request.url, db)
        
        logger.info(f"Analysis complete: {result.scan_id}")
        
        return result
    
    except ValueError as e:
        logger.warning(f"Invalid URL: {e}")
        raise HTTPException(
            status_code=400,
            detail="Invalid URL format. Please provide a valid URL starting with http:// or https://"
        )
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during URL analysis"
        )


@router.get("/scans", response_model=ScansList, status_code=200)
async def get_scans(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    risk_level: str = Query(None, description="Filter by risk level (LOW, MODERATE, SUSPICIOUS, HIGH)"),
    db: Session = Depends(get_db)
):
    """
    Get all scan records with optional filtering
    
    **Endpoint:** `GET /api/scans`
    
    **Query Parameters:**
    - `skip` (int): Records to skip (default: 0)
    - `limit` (int): Records to return (default: 50, max: 100)
    - `risk_level` (str): Filter by risk level
    
    **Response:**
    ```json
    {
        "total": 100,
        "scans": [...]
    }
    ```
    """
    try:
        logger.info(f"Retrieving scans: skip={skip}, limit={limit}")
        
        scans = DatabaseService.get_all_scans(db, skip, limit, risk_level)
        
        return scans
    
    except Exception as e:
        logger.error(f"Error retrieving scans: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving scans"
        )


@router.get("/scans/search", response_model=ScansList, status_code=200)
async def search_scans(
    query: str = Query(..., min_length=1, description="URL to search for"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search scans by URL
    
    **Endpoint:** `GET /api/scans/search`
    
    **Query Parameters:**
    - `query` (str): URL to search for (required)
    - `skip` (int): Records to skip
    - `limit` (int): Records to return
    """
    try:
        logger.info(f"Searching scans: query={query}")
        
        results = DatabaseService.search_scans(db, query, skip, limit)
        
        return results
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during search"
        )


@router.get("/scans/{scan_id}", response_model=AnalyzeResponse, status_code=200)
async def get_scan(
    scan_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific scan by ID
    
    **Endpoint:** `GET /api/scans/{scan_id}`
    
    **Path Parameters:**
    - `scan_id` (str): Unique scan identifier (UUID)
    
    **Response:** Complete scan analysis result
    
    **Status Codes:**
    - `200`: Scan found
    - `404`: Scan not found
    """
    try:
        logger.info(f"Retrieving scan: {scan_id}")
        
        scan = DatabaseService.get_scan_by_id(db, scan_id)
        
        if not scan:
            raise HTTPException(
                status_code=404,
                detail="Scan not found"
            )
        
        return scan
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving scan: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the scan"
        )


@router.delete("/scans/{scan_id}", status_code=204)
async def delete_scan(
    scan_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a specific scan
    
    **Endpoint:** `DELETE /api/scans/{scan_id}`
    
    **Path Parameters:**
    - `scan_id` (str): Unique scan identifier
    
    **Status Codes:**
    - `204`: Scan deleted successfully
    - `404`: Scan not found
    """
    try:
        logger.info(f"Deleting scan: {scan_id}")
        
        success = DatabaseService.delete_scan(db, scan_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Scan not found"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting scan: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the scan"
        )


@router.delete("/scans", status_code=204)
async def delete_all_scans(
    db: Session = Depends(get_db)
):
    """
    Delete all scan records (use with caution)
    
    **Endpoint:** `DELETE /api/scans`
    
    **Status Codes:**
    - `204`: All scans deleted successfully
    """
    try:
        logger.warning("Deleting all scans")
        
        count = DatabaseService.delete_all_scans(db)
        
        logger.info(f"Deleted {count} scans")
    
    except Exception as e:
        logger.error(f"Error deleting all scans: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting scans"
        )


@router.get("/statistics", response_model=Statistics, status_code=200)
async def get_statistics(
    db: Session = Depends(get_db)
):
    """
    Get application statistics
    
    **Endpoint:** `GET /api/statistics`
    
    **Response:**
    ```json
    {
        "total_scans": 100,
        "safe_scans": 45,
        "moderate_scans": 30,
        "suspicious_scans": 15,
        "high_risk_scans": 10,
        "average_risk_score": 38.5
    }
    ```
    """
    try:
        logger.info("Retrieving statistics")
        
        stats = StatisticsService.get_statistics(db)
        
        return stats
    
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving statistics"
        )


@router.get("/health", response_model=HealthResponse, status_code=200)
async def health_check(
    db: Session = Depends(get_db)
):
    """
    Health check endpoint
    
    **Endpoint:** `GET /api/health`
    
    **Response:**
    ```json
    {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2024-01-15T10:30:00",
        "database": "connected"
    }
    ```
    
    **Status Codes:**
    - `200`: Service is healthy
    - `503`: Service is unhealthy
    """
    try:
        logger.debug("Health check requested")
        
        # Try to connect to database
        db.execute("SELECT 1")
        database_status = "connected"
        
        return HealthResponse(
            status="healthy",
            version=settings.API_VERSION,
            timestamp=datetime.utcnow(),
            database=database_status
        )
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service is unhealthy"
        )
