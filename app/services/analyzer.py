# PhishGuard - URL Analyzer Service
# Main business logic for URL analysis

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.utils.url_parser import URLParser
from app.utils.feature_extractor import FeatureExtractor
from app.services.scoring_engine import RiskScoringEngine
from app.models.models import Scan
from app.schemas.schemas import AnalyzeResponse, ScoringBreakdown
from app.core.logging_config import logger
import json


class URLAnalyzerService:
    """Main service for URL analysis"""
    
    @staticmethod
    def analyze_url(url: str, db: Optional[Session] = None) -> AnalyzeResponse:
        """
        Analyze URL for phishing risk
        
        Args:
            url: URL to analyze
            db: Database session (optional)
            
        Returns:
            AnalyzeResponse with complete analysis
        """
        try:
            # Validate URL
            if not URLParser.is_valid_url(url):
                raise ValueError("Invalid URL format")
            
            # Generate unique scan ID
            scan_id = str(uuid.uuid4())
            
            # Normalize URL
            normalized_url = URLParser.normalize_url(url)
            
            # Extract features
            features = FeatureExtractor.extract_all_features(normalized_url)
            
            # Calculate risk score
            score, risk_level, indicators = RiskScoringEngine.calculate_risk_score(features)
            
            # Generate score breakdown
            breakdown = RiskScoringEngine.generate_score_breakdown(features, score)
            breakdown_models = [
                ScoringBreakdown(
                    feature=item["feature"],
                    weight=item["weight"],
                    reason=item["reason"]
                )
                for item in breakdown
            ]
            
            # Generate recommendations
            recommendations = RiskScoringEngine.generate_recommendations(
                score, risk_level, indicators
            )
            
            # Prepare technical details
            technical_details = {
                "url_length": features.get("url_length", 0),
                "domain": features.get("domain", ""),
                "domain_length": features.get("domain_length", 0),
                "subdomain_count": features.get("subdomain_count", 0),
                "uses_https": features.get("uses_https", False),
                "uses_http": features.get("uses_http", False),
                "is_ip_based": features.get("is_ip_based", False),
                "is_url_shortener": features.get("is_url_shortener", False),
                "has_punycode": features.get("has_punycode", False),
                "dot_count": features.get("dot_count", 0),
                "special_char_count": features.get("special_char_count", 0),
                "query_param_count": features.get("query_param_count", 0),
            }
            
            # Create response
            response = AnalyzeResponse(
                scan_id=scan_id,
                url=normalized_url,
                risk_score=score,
                risk_level=risk_level,
                indicators=indicators,
                scoring_breakdown=breakdown_models,
                recommendations=recommendations,
                technical_details=technical_details,
                timestamp=datetime.utcnow()
            )
            
            # Save to database if session provided
            if db:
                URLAnalyzerService._save_scan(
                    db, scan_id, normalized_url, score, risk_level,
                    indicators, breakdown, recommendations, features
                )
            
            logger.info(f"URL analyzed: {scan_id} - Risk: {risk_level}")
            
            return response
        
        except ValueError as e:
            logger.warning(f"URL validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"URL analysis error: {e}")
            raise
    
    @staticmethod
    def _save_scan(
        db: Session,
        scan_id: str,
        url: str,
        score: float,
        risk_level: str,
        indicators: list,
        breakdown: list,
        recommendations: str,
        features: dict
    ) -> Scan:
        """Save scan to database"""
        try:
            scan = Scan(
                scan_id=scan_id,
                url=url,
                risk_score=score,
                risk_level=risk_level,
                detected_features=json.dumps(indicators),
                scoring_breakdown=json.dumps(breakdown),
                recommendations=recommendations,
                domain=features.get("domain", ""),
                domain_length=features.get("domain_length", 0),
                url_length=features.get("url_length", 0),
                created_at=datetime.utcnow()
            )
            
            db.add(scan)
            db.commit()
            db.refresh(scan)
            
            logger.debug(f"Scan saved to database: {scan_id}")
            
            return scan
        
        except Exception as e:
            logger.error(f"Database save error: {e}")
            db.rollback()
            raise
