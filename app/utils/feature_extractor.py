# PhishGuard - Feature Extraction
# Extract security-related features from URLs

import re
from typing import Dict, List, Tuple
from app.utils.url_parser import URLParser
from app.core.config import (
    SUSPICIOUS_KEYWORDS, PUNYCODE_PREFIX, MAX_SUBDOMAINS,
    MAX_DOTS_IN_URL, EXCESSIVE_REDIRECT_COUNT
)
from app.core.logging_config import logger


class FeatureExtractor:
    """Extract security features from URLs"""
    
    @staticmethod
    def extract_all_features(url: str) -> Dict[str, any]:
        """
        Extract all security features from URL
        
        Args:
            url: URL to analyze
            
        Returns:
            Dictionary of extracted features
        """
        try:
            # Normalize URL
            normalized_url = URLParser.normalize_url(url)
            
            features = {
                # Basic metrics
                "url_length": len(normalized_url),
                "url": normalized_url,
                
                # Domain features
                "domain": URLParser.extract_domain(normalized_url),
                "domain_length": len(URLParser.extract_domain(normalized_url) or ""),
                "subdomain_count": URLParser.count_subdomains(normalized_url),
                
                # URL structure
                "dot_count": normalized_url.count('.'),
                "hyphen_count": normalized_url.count('-'),
                "underscore_count": normalized_url.count('_'),
                "special_char_count": URLParser.count_special_characters(normalized_url),
                
                # Protocol and security
                "uses_https": normalized_url.startswith('https://'),
                "uses_http": normalized_url.startswith('http://'),
                
                # IP-based detection
                "is_ip_based": URLParser.is_ip_based_url(normalized_url),
                
                # Shortener detection
                "is_url_shortener": URLParser.is_url_shortener(normalized_url),
                
                # Punycode/IDN detection
                "has_punycode": FeatureExtractor._has_punycode(normalized_url),
                
                # Suspicious keyword detection
                "suspicious_keywords": FeatureExtractor._detect_suspicious_keywords(normalized_url),
                
                # Query parameters
                "query_param_count": len(URLParser.extract_query_parameters(normalized_url)),
                "has_suspicious_params": FeatureExtractor._has_suspicious_query_params(normalized_url),
                
                # Path analysis
                "path": URLParser.extract_components(normalized_url).get('path', ''),
                "path_depth": normalized_url.count('/') - 3,  # Subtract protocol and initial slashes
            }
            
            return features
        except Exception as e:
            logger.error(f"Feature extraction error: {e}")
            return {}
    
    @staticmethod
    def _has_punycode(url: str) -> bool:
        """Check if URL contains punycode (IDN)"""
        try:
            return PUNYCODE_PREFIX.lower() in url.lower()
        except Exception as e:
            logger.warning(f"Punycode detection error: {e}")
            return False
    
    @staticmethod
    def _detect_suspicious_keywords(url: str) -> List[str]:
        """Detect suspicious keywords in URL"""
        try:
            url_lower = url.lower()
            detected = []
            
            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword in url_lower:
                    detected.append(keyword)
            
            return detected
        except Exception as e:
            logger.warning(f"Keyword detection error: {e}")
            return []
    
    @staticmethod
    def _has_suspicious_query_params(url: str) -> bool:
        """Check for suspicious query parameters"""
        try:
            params = URLParser.extract_query_parameters(url)
            suspicious_param_keywords = ['redirect', 'url', 'return', 'link', 'target']
            
            for param_name in params.keys():
                if any(keyword in param_name.lower() for keyword in suspicious_param_keywords):
                    return True
            
            return False
        except Exception as e:
            logger.warning(f"Suspicious param detection error: {e}")
            return False
    
    @staticmethod
    def calculate_feature_statistics(features: Dict) -> Dict:
        """Calculate statistics from extracted features"""
        try:
            return {
                "total_dots": features.get("dot_count", 0),
                "total_hyphens": features.get("hyphen_count", 0),
                "total_underscores": features.get("underscore_count", 0),
                "total_special_chars": features.get("special_char_count", 0),
                "suspicious_keywords_found": len(features.get("suspicious_keywords", [])),
                "query_params_count": features.get("query_param_count", 0),
            }
        except Exception as e:
            logger.warning(f"Statistics calculation error: {e}")
            return {}
