# PhishGuard - Comprehensive Tests
# Test suite for URL analysis and security features

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base, get_db
from app.utils.url_parser import URLParser
from app.utils.feature_extractor import FeatureExtractor
from app.services.scoring_engine import RiskScoringEngine

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestURLParser:
    """Test URL parsing and validation"""
    
    def test_valid_url(self):
        """Test valid URL detection"""
        assert URLParser.is_valid_url("https://example.com")
        assert URLParser.is_valid_url("http://example.com/login")
        assert URLParser.is_valid_url("https://sub.example.com/path?query=value")
    
    def test_invalid_url(self):
        """Test invalid URL detection"""
        assert not URLParser.is_valid_url("not a url")
        assert not URLParser.is_valid_url("example.com")
        assert not URLParser.is_valid_url("")
        assert not URLParser.is_valid_url("ftp://example.com" if "ftp" not in ["http", "https"] else True)
    
    def test_url_normalization(self):
        """Test URL normalization"""
        url = "HTTPS://EXAMPLE.COM/PATH"
        normalized = URLParser.normalize_url(url)
        assert normalized.startswith("https://")
        assert "example.com" in normalized
    
    def test_ip_based_url_detection(self):
        """Test IP address detection"""
        assert URLParser.is_ip_based_url("http://192.168.1.1")
        assert URLParser.is_ip_based_url("http://127.0.0.1:8000")
        assert not URLParser.is_ip_based_url("https://example.com")
    
    def test_domain_extraction(self):
        """Test domain extraction"""
        domain = URLParser.extract_domain("https://www.example.com/path")
        assert domain == "example.com"
    
    def test_subdomain_counting(self):
        """Test subdomain counting"""
        assert URLParser.count_subdomains("https://example.com") == 0
        assert URLParser.count_subdomains("https://sub.example.com") == 1
        assert URLParser.count_subdomains("https://a.b.c.example.com") == 3
    
    def test_url_shortener_detection(self):
        """Test URL shortener detection"""
        assert URLParser.is_url_shortener("https://bit.ly/abc123")
        assert URLParser.is_url_shortener("https://tinyurl.com/xyz")
        assert not URLParser.is_url_shortener("https://example.com")


class TestFeatureExtractor:
    """Test feature extraction"""
    
    def test_feature_extraction(self):
        """Test basic feature extraction"""
        url = "https://example.com/login"
        features = FeatureExtractor.extract_all_features(url)
        
        assert "url_length" in features
        assert "domain" in features
        assert "uses_https" in features
        assert features["uses_https"] is True
    
    def test_suspicious_keyword_detection(self):
        """Test suspicious keyword detection"""
        url = "https://example.com/login-verify"
        features = FeatureExtractor.extract_all_features(url)
        
        assert len(features["suspicious_keywords"]) > 0
        assert "login" in features["suspicious_keywords"]
    
    def test_no_suspicious_keywords(self):
        """Test URL without suspicious keywords"""
        url = "https://example.com/products"
        features = FeatureExtractor.extract_all_features(url)
        
        assert len(features["suspicious_keywords"]) == 0


class TestRiskScoringEngine:
    """Test risk scoring"""
    
    def test_low_risk_score(self):
        """Test low risk URL"""
        features = {
            "is_ip_based": False,
            "suspicious_keywords": [],
            "subdomain_count": 0,
            "url_length": 30,
            "has_suspicious_params": False,
            "uses_https": True,
            "has_punycode": False,
            "is_url_shortener": False,
            "dot_count": 2,
            "special_char_count": 0,
        }
        score, level, indicators = RiskScoringEngine.calculate_risk_score(features)
        
        assert score <= 25
        assert level == "LOW"
    
    def test_high_risk_score(self):
        """Test high risk URL"""
        features = {
            "is_ip_based": True,
            "suspicious_keywords": ["login", "verify"],
            "subdomain_count": 5,
            "url_length": 200,
            "has_suspicious_params": True,
            "uses_https": False,
            "has_punycode": True,
            "is_url_shortener": True,
            "dot_count": 10,
            "special_char_count": 15,
        }
        score, level, indicators = RiskScoringEngine.calculate_risk_score(features)
        
        assert score >= 76
        assert level == "HIGH"
    
    def test_risk_level_classification(self):
        """Test risk level classification"""
        assert RiskScoringEngine.get_risk_level(10) == "LOW"
        assert RiskScoringEngine.get_risk_level(30) == "MODERATE"
        assert RiskScoringEngine.get_risk_level(60) == "SUSPICIOUS"
        assert RiskScoringEngine.get_risk_level(85) == "HIGH"


class TestAPIEndpoints:
    """Test FastAPI endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_analyze_valid_url(self):
        """Test URL analysis endpoint"""
        response = client.post(
            "/api/analyze",
            json={"url": "https://example.com/login"}
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "scan_id" in data
        assert "risk_score" in data
        assert "risk_level" in data
        assert "indicators" in data
        assert "recommendations" in data
        assert 0 <= data["risk_score"] <= 100
    
    def test_analyze_invalid_url(self):
        """Test invalid URL handling"""
        response = client.post(
            "/api/analyze",
            json={"url": "not a valid url"}
        )
        assert response.status_code == 400
    
    def test_get_statistics(self):
        """Test statistics endpoint"""
        response = client.get("/api/statistics")
        assert response.status_code == 200
        data = response.json()
        
        assert "total_scans" in data
        assert "safe_scans" in data
        assert "average_risk_score" in data
    
    def test_get_scans(self):
        """Test scan history endpoint"""
        response = client.get("/api/scans")
        assert response.status_code == 200
        data = response.json()
        
        assert "total" in data
        assert "scans" in data
        assert isinstance(data["scans"], list)
    
    def test_analyze_and_retrieve(self):
        """Test analyzing URL and retrieving results"""
        # Analyze URL
        analyze_response = client.post(
            "/api/analyze",
            json={"url": "https://test.example.com"}
        )
        assert analyze_response.status_code == 200
        scan_id = analyze_response.json()["scan_id"]
        
        # Retrieve scan
        get_response = client.get(f"/api/scans/{scan_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["scan_id"] == scan_id
    
    def test_delete_scan(self):
        """Test deleting a scan"""
        # Analyze URL
        analyze_response = client.post(
            "/api/analyze",
            json={"url": "https://delete-test.example.com"}
        )
        scan_id = analyze_response.json()["scan_id"]
        
        # Delete scan
        delete_response = client.delete(f"/api/scans/{scan_id}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/scans/{scan_id}")
        assert get_response.status_code == 404


class TestInputValidation:
    """Test input validation and security"""
    
    def test_url_length_limit(self):
        """Test URL length validation"""
        long_url = "https://" + "a" * 3000
        response = client.post(
            "/api/analyze",
            json={"url": long_url}
        )
        assert response.status_code == 400
    
    def test_empty_url(self):
        """Test empty URL handling"""
        response = client.post(
            "/api/analyze",
            json={"url": ""}
        )
        assert response.status_code == 400
    
    def test_special_characters(self):
        """Test URL with special characters"""
        response = client.post(
            "/api/analyze",
            json={"url": "https://example.com/path?id=123&name=test&special=!@#$%"}
        )
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
