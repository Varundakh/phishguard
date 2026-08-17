# PhishGuard - Risk Scoring Engine
# Calculate phishing risk scores based on extracted features

import json
from typing import Dict, List, Tuple
from app.core.config import SCORING_WEIGHTS, RISK_SCORE_RANGES, RISK_CATEGORIES
from app.core.logging_config import logger


class RiskScoringEngine:
    """Calculate phishing risk scores"""
    
    @staticmethod
    def calculate_risk_score(features: Dict) -> Tuple[float, str, List[str]]:
        """
        Calculate risk score from features
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            Tuple of (risk_score, risk_level, indicators)
        """
        try:
            score = 0
            indicators = []
            
            # IP-based URL (high risk)
            if features.get("is_ip_based"):
                score += SCORING_WEIGHTS["ip_address"]
                indicators.append("IP address used instead of domain")
            
            # Suspicious keywords
            keywords = features.get("suspicious_keywords", [])
            if keywords:
                score += SCORING_WEIGHTS["suspicious_keyword"] * min(len(keywords), 2)
                indicators.append(f"Suspicious keywords found: {', '.join(keywords[:3])}")
            
            # Excessive subdomains
            subdomain_count = features.get("subdomain_count", 0)
            if subdomain_count > 3:
                score += SCORING_WEIGHTS["excessive_subdomains"]
                indicators.append(f"Excessive subdomains ({subdomain_count})")
            
            # Long URL
            url_length = features.get("url_length", 0)
            if url_length > 75:
                score += SCORING_WEIGHTS["long_url"]
                indicators.append("Unusually long URL")
            
            # Suspicious query parameters
            if features.get("has_suspicious_params"):
                score += SCORING_WEIGHTS["suspicious_query_params"]
                indicators.append("Suspicious query parameters detected")
            
            # No HTTPS
            if not features.get("uses_https"):
                score += SCORING_WEIGHTS["no_https"]
                indicators.append("URL does not use HTTPS protocol")
            
            # Punycode/IDN
            if features.get("has_punycode"):
                score += SCORING_WEIGHTS["punycode_domain"]
                indicators.append("Punycode/IDN domain detected")
            
            # URL Shortener
            if features.get("is_url_shortener"):
                score += SCORING_WEIGHTS["url_shortener"]
                indicators.append("URL uses shortening service")
            
            # Excessive dots
            dot_count = features.get("dot_count", 0)
            if dot_count > 5:
                score += SCORING_WEIGHTS["excessive_dots"]
                indicators.append("Excessive dots in URL")
            
            # Special characters
            special_chars = features.get("special_char_count", 0)
            if special_chars > 10:
                score += SCORING_WEIGHTS["special_characters"]
                indicators.append("Excessive special characters")
            
            # Ensure score is within bounds
            score = min(max(score, 0), 100)
            
            # Determine risk level
            risk_level = RiskScoringEngine.get_risk_level(score)
            
            return score, risk_level, indicators
        
        except Exception as e:
            logger.error(f"Risk scoring error: {e}")
            return 50, "SUSPICIOUS", ["Error during analysis"]
    
    @staticmethod
    def get_risk_level(score: float) -> str:
        """
        Get risk level from score
        
        Args:
            score: Risk score (0-100)
            
        Returns:
            Risk level string
        """
        for level, (min_score, max_score) in RISK_SCORE_RANGES.items():
            if min_score <= score <= max_score:
                return level
        
        return "HIGH"
    
    @staticmethod
    def generate_score_breakdown(features: Dict, score: float) -> List[Dict]:
        """
        Generate detailed breakdown of score calculation
        
        Args:
            features: Extracted features
            score: Final score
            
        Returns:
            List of scoring components
        """
        try:
            breakdown = []
            
            # IP-based URL
            if features.get("is_ip_based"):
                breakdown.append({
                    "feature": "IP-based URL",
                    "weight": SCORING_WEIGHTS["ip_address"],
                    "reason": "URLs using IP addresses instead of domains are often used in phishing"
                })
            
            # Suspicious keywords
            keywords = features.get("suspicious_keywords", [])
            if keywords:
                weight = SCORING_WEIGHTS["suspicious_keyword"] * min(len(keywords), 2)
                breakdown.append({
                    "feature": "Suspicious Keywords",
                    "weight": weight,
                    "reason": f"Detected phishing-related keywords: {', '.join(keywords[:3])}"
                })
            
            # Excessive subdomains
            if features.get("subdomain_count", 0) > 3:
                breakdown.append({
                    "feature": "Excessive Subdomains",
                    "weight": SCORING_WEIGHTS["excessive_subdomains"],
                    "reason": "Multiple subdomains can obscure the real domain"
                })
            
            # Long URL
            if features.get("url_length", 0) > 75:
                breakdown.append({
                    "feature": "Long URL",
                    "weight": SCORING_WEIGHTS["long_url"],
                    "reason": "Excessively long URLs may hide malicious intent"
                })
            
            # No HTTPS
            if not features.get("uses_https"):
                breakdown.append({
                    "feature": "Missing HTTPS",
                    "weight": SCORING_WEIGHTS["no_https"],
                    "reason": "Unencrypted connection - credentials could be intercepted"
                })
            
            return breakdown
        
        except Exception as e:
            logger.warning(f"Breakdown generation error: {e}")
            return []
    
    @staticmethod
    def generate_recommendations(score: float, risk_level: str, indicators: List[str]) -> str:
        """
        Generate security recommendations based on analysis
        
        Args:
            score: Risk score
            risk_level: Risk level
            indicators: List of detected indicators
            
        Returns:
            Recommendation text
        """
        try:
            if risk_level == "HIGH":
                return (
                    "🚨 HIGH RISK - Do NOT enter any personal information, passwords, "
                    "OTPs, or banking details into this website. "
                    "Verify the legitimate website domain independently through an official channel. "
                    "If this is an unexpected link, it may be a phishing attempt."
                )
            elif risk_level == "SUSPICIOUS":
                return (
                    "⚠️ SUSPICIOUS - Exercise extreme caution before entering sensitive information. "
                    "Verify the website's legitimacy independently. "
                    "Contact the organization directly using a phone number or address from official sources."
                )
            elif risk_level == "MODERATE":
                return (
                    "⚠️ MODERATE RISK - Verify website details before entering sensitive information. "
                    "Check the URL carefully and ensure you're on the legitimate website."
                )
            else:  # LOW
                return (
                    "✅ LOW RISK - This URL appears safe based on initial analysis. "
                    "However, always practice good security hygiene and verify sensitive transactions."
                )
        
        except Exception as e:
            logger.warning(f"Recommendation generation error: {e}")
            return "Unable to generate recommendations"
