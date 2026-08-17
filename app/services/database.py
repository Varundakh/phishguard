# PhishGuard - Database Service
# Database operations and queries

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.models.models import Scan
from app.schemas.schemas import ScanRecord, ScansList
from app.core.logging_config import logger


class DatabaseService:
    """Handle database operations"""
    
    @staticmethod
    def get_scan_by_id(db: Session, scan_id: str) -> Optional[ScanRecord]:
        """Get scan by ID"""
        try:
            scan = db.query(Scan).filter(Scan.scan_id == scan_id).first()
            if scan:
                return ScanRecord.from_orm(scan)
            return None
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return None
    
    @staticmethod
    def get_all_scans(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        risk_level: Optional[str] = None
    ) -> ScansList:
        """Get all scans with optional filtering"""
        try:
            query = db.query(Scan).order_by(desc(Scan.created_at))
            
            # Filter by risk level if provided
            if risk_level:
                query = query.filter(Scan.risk_level == risk_level)
            
            total = query.count()
            scans = query.offset(skip).limit(limit).all()
            
            return ScansList(
                total=total,
                scans=[ScanRecord.from_orm(scan) for scan in scans]
            )
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return ScansList(total=0, scans=[])
    
    @staticmethod
    def search_scans(db: Session, query: str, skip: int = 0, limit: int = 50) -> ScansList:
        """Search scans by URL"""
        try:
            scans = db.query(Scan).filter(
                Scan.url.ilike(f"%{query}%")
            ).order_by(desc(Scan.created_at)).offset(skip).limit(limit).all()
            
            total = db.query(Scan).filter(
                Scan.url.ilike(f"%{query}%")
            ).count()
            
            return ScansList(
                total=total,
                scans=[ScanRecord.from_orm(scan) for scan in scans]
            )
        except Exception as e:
            logger.error(f"Search error: {e}")
            return ScansList(total=0, scans=[])
    
    @staticmethod
    def delete_scan(db: Session, scan_id: str) -> bool:
        """Delete a scan record"""
        try:
            scan = db.query(Scan).filter(Scan.scan_id == scan_id).first()
            if scan:
                db.delete(scan)
                db.commit()
                logger.info(f"Scan deleted: {scan_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Delete error: {e}")
            db.rollback()
            return False
    
    @staticmethod
    def delete_all_scans(db: Session) -> int:
        """Delete all scan records"""
        try:
            count = db.query(Scan).delete()
            db.commit()
            logger.info(f"All scans deleted: {count} records")
            return count
        except Exception as e:
            logger.error(f"Delete all error: {e}")
            db.rollback()
            return 0
