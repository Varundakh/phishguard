# PhishGuard - Pydantic Schemas
# Request/response validation schemas

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AnalyzeRequest(BaseModel):
    """Request schema for URL analysis"""
    url: str = Field(
        ...,
        min_length=10,
        max_length=2048,
        description="URL to analyze"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/login"
            }
        }


class ScoringBreakdown(BaseModel):
    """Individual scoring component"""
    feature: str
    weight: int
    reason: str


class AnalyzeResponse(BaseModel):
    """Response schema for URL analysis"""
    scan_id: str
    url: str
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    
    indicators: List[str] = []
    scoring_breakdown: Optional[List[ScoringBreakdown]] = None
    recommendations: str
    
    technical_details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "scan_id": "550e8400-e29b-41d4-a716-446655440000",
                "url": "https://example.com/login",
                "risk_score": 42,
                "risk_level": "MODERATE",
                "indicators": ["Missing security headers", "Long URL"],
                "recommendations": "Verify domain independently before entering credentials",
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class ScanRecord(BaseModel):
    """Database scan record"""
    id: int
    scan_id: str
    url: str
    risk_score: float
    risk_level: str
    detected_features: Optional[str] = None
    recommendations: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ScansList(BaseModel):
    """List of scan records"""
    total: int
    scans: List[ScanRecord]


class Statistics(BaseModel):
    """Statistics response"""
    total_scans: int
    safe_scans: int
    moderate_scans: int
    suspicious_scans: int
    high_risk_scans: int
    average_risk_score: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_scans": 100,
                "safe_scans": 45,
                "moderate_scans": 30,
                "suspicious_scans": 15,
                "high_risk_scans": 10,
                "average_risk_score": 38.5
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    database: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime
