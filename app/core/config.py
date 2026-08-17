# PhishGuard - Core Configuration
# This file contains all configuration constants and settings

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./phishguard.db"
    
    # FastAPI
    DEBUG: bool = True
    API_TITLE: str = "PhishGuard API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Intelligent Phishing URL & Website Risk Analyzer"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/phishguard.log"
    
    # ML Model
    USE_ML_CLASSIFIER: bool = False
    ML_MODEL_PATH: str = "ml/models/phishing_classifier.pkl"
    
    # Feature Extraction
    MAX_URL_LENGTH: int = 2048
    MIN_URL_LENGTH: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Risk Score Constants
RISK_SCORE_RANGES = {
    "LOW": (0, 25),
    "MODERATE": (26, 50),
    "SUSPICIOUS": (51, 75),
    "HIGH": (76, 100),
}

RISK_CATEGORIES = {
    "LOW": "Safe",
    "MODERATE": "Moderate Risk",
    "SUSPICIOUS": "Suspicious",
    "HIGH": "High Risk / Phishing",
}

# Suspicious Keywords (commonly used in phishing URLs)
SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "confirm", "update", "security",
    "account", "validate", "authenticate", "paypal", "amazon", "apple",
    "google", "microsoft", "bank", "password", "reset", "urgent",
    "action", "alert", "click", "activate", "suspended", "limited",
    "restricted", "unusual", "confirm-identity", "verify-account"
]

# URL Pattern Constants
IP_ADDRESS_PATTERN = r"^(\d{1,3}\.){3}\d{1,3}"
PUNYCODE_PREFIX = "xn--"
SHORTENER_DOMAINS = [
    "bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "short.link",
    "buff.ly", "rebrand.ly", "adf.ly", "tiny.cc", "is.gd"
]

# Feature Extraction Limits
MAX_SUBDOMAINS = 3
MAX_DOTS_IN_URL = 5
MAX_SPECIAL_CHARS = 10
EXCESSIVE_REDIRECT_COUNT = 5

# Scoring Weights for Rule-Based Detection
SCORING_WEIGHTS = {
    "ip_address": 20,
    "suspicious_keyword": 15,
    "excessive_subdomains": 10,
    "long_url": 15,
    "suspicious_query_params": 12,
    "no_https": 18,
    "punycode_domain": 16,
    "url_shortener": 14,
    "excessive_dots": 8,
    "unusual_port": 10,
    "special_characters": 9,
    "domain_age_new": 7,
}

# HTTP Methods
ALLOWED_HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

# Security Headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
}
