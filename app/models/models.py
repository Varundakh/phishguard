# PhishGuard - Database Models
# SQLAlchemy ORM models for scan history and results

from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from app.database.database import Base


class Scan(Base):
    """Database model for URL scan results"""
    
    __tablename__ = "scans"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Scan metadata
    scan_id = Column(String(36), unique=True, nullable=False, index=True)
    url = Column(String(2048), nullable=False, index=True)
    
    # Risk assessment
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False, index=True)
    
    # Detailed analysis
    detected_features = Column(Text, nullable=True)  # JSON string
    scoring_breakdown = Column(Text, nullable=True)  # JSON string
    recommendations = Column(Text, nullable=True)
    
    # Technical details
    domain = Column(String(255), nullable=True)
    domain_length = Column(Integer, nullable=True)
    url_length = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Scan(id={self.id}, url={self.url}, risk_level={self.risk_level})>"
