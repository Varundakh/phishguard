# PhishGuard - Statistics Service
# Generate statistics and analytics

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Scan
from app.schemas.schemas import Statistics
from app.core.logging_config import logger


class StatisticsService:
    """Generate application statistics"""
    
    @staticmethod
    def get_statistics(db: Session) -> Statistics:
        """
        Get application statistics
        
        Args:
            db: Database session
            
        Returns:
            Statistics object
        """
        try:
            # Get all scans
            total_scans = db.query(Scan).count()
            
            if total_scans == 0:
                return Statistics(
                    total_scans=0,
                    safe_scans=0,
                    moderate_scans=0,
                    suspicious_scans=0,
                    high_risk_scans=0,
                    average_risk_score=0.0
                )
            
            # Count by risk level
            safe_scans = db.query(Scan).filter(Scan.risk_level == "LOW").count()
            moderate_scans = db.query(Scan).filter(Scan.risk_level == "MODERATE").count()
            suspicious_scans = db.query(Scan).filter(Scan.risk_level == "SUSPICIOUS").count()
            high_risk_scans = db.query(Scan).filter(Scan.risk_level == "HIGH").count()
            
            # Calculate average score
            avg_score = db.query(func.avg(Scan.risk_score)).scalar() or 0.0
            
            stats = Statistics(
                total_scans=total_scans,
                safe_scans=safe_scans,
                moderate_scans=moderate_scans,
                suspicious_scans=suspicious_scans,
                high_risk_scans=high_risk_scans,
                average_risk_score=float(avg_score)
            )
            
            logger.info(f"Statistics generated: {total_scans} scans")
            
            return stats
        
        except Exception as e:
            logger.error(f"Statistics generation error: {e}")
            return Statistics(
                total_scans=0,
                safe_scans=0,
                moderate_scans=0,
                suspicious_scans=0,
                high_risk_scans=0,
                average_risk_score=0.0
            )
