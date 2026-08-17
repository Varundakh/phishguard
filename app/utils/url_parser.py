# PhishGuard - URL Utilities
# URL parsing, validation, and normalization

import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, Tuple, Optional
from app.core.config import IP_ADDRESS_PATTERN, SHORTENER_DOMAINS
from app.core.logging_config import logger


class URLParser:
    """Safe URL parsing and validation"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validate URL format
        
        Args:
            url: URL string to validate
            
        Returns:
            True if URL is valid, False otherwise
        """
        try:
            # Basic format check
            if not url or len(url) < 10 or len(url) > 2048:
                return False
            
            # Check for valid scheme
            if not url.startswith(('http://', 'https://', 'ftp://')):
                return False
            
            # Parse URL
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception as e:
            logger.warning(f"URL validation error: {e}")
            return False
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize URL for consistent analysis
        
        Args:
            url: URL string to normalize
            
        Returns:
            Normalized URL
        """
        try:
            # Remove trailing slashes
            url = url.rstrip('/')
            
            # Lowercase the scheme and domain
            parsed = urlparse(url)
            normalized = f"{parsed.scheme}://{parsed.netloc.lower()}{parsed.path}"
            
            if parsed.query:
                normalized += f"?{parsed.query}"
            if parsed.fragment:
                normalized += f"#{parsed.fragment}"
            
            return normalized
        except Exception as e:
            logger.warning(f"URL normalization error: {e}")
            return url
    
    @staticmethod
    def extract_components(url: str) -> Dict[str, any]:
        """
        Extract URL components for analysis
        
        Args:
            url: URL string to parse
            
        Returns:
            Dictionary with URL components
        """
        try:
            parsed = urlparse(url)
            
            return {
                "scheme": parsed.scheme,
                "netloc": parsed.netloc,
                "domain": parsed.netloc.split(':')[0],  # Remove port
                "path": parsed.path,
                "query": parsed.query,
                "fragment": parsed.fragment,
                "port": parsed.port,
                "hostname": parsed.hostname,
                "username": parsed.username,
                "password": parsed.password,
            }
        except Exception as e:
            logger.error(f"Error extracting URL components: {e}")
            return {}
    
    @staticmethod
    def is_ip_based_url(url: str) -> bool:
        """
        Check if URL uses IP address instead of domain
        
        Args:
            url: URL string to check
            
        Returns:
            True if URL uses IP address
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.split(':')[0]  # Remove port
            
            # Check for IPv4 pattern
            if re.match(IP_ADDRESS_PATTERN, domain):
                return True
            
            # Check for localhost or IPv6
            if domain in ['localhost', '127.0.0.1'] or domain.startswith('['):
                return True
            
            return False
        except Exception as e:
            logger.warning(f"IP check error: {e}")
            return False
    
    @staticmethod
    def extract_domain(url: str) -> Optional[str]:
        """
        Extract domain from URL
        
        Args:
            url: URL string
            
        Returns:
            Domain name or None
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.split(':')[0]  # Remove port
            
            # Remove www prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return domain
        except Exception as e:
            logger.warning(f"Domain extraction error: {e}")
            return None
    
    @staticmethod
    def count_subdomains(url: str) -> int:
        """
        Count number of subdomains
        
        Args:
            url: URL string
            
        Returns:
            Number of subdomains
        """
        try:
            domain = URLParser.extract_domain(url)
            if not domain:
                return 0
            
            # Count dots in domain (subdomains)
            return domain.count('.')
        except Exception as e:
            logger.warning(f"Subdomain count error: {e}")
            return 0
    
    @staticmethod
    def extract_query_parameters(url: str) -> Dict[str, list]:
        """
        Extract query parameters from URL
        
        Args:
            url: URL string
            
        Returns:
            Dictionary of query parameters
        """
        try:
            parsed = urlparse(url)
            return parse_qs(parsed.query)
        except Exception as e:
            logger.warning(f"Query parameter extraction error: {e}")
            return {}
    
    @staticmethod
    def is_url_shortener(url: str) -> bool:
        """
        Check if URL uses a shortening service
        
        Args:
            url: URL string
            
        Returns:
            True if URL is from known shortener
        """
        try:
            domain = URLParser.extract_domain(url)
            if not domain:
                return False
            
            for shortener in SHORTENER_DOMAINS:
                if shortener in domain.lower():
                    return True
            
            return False
        except Exception as e:
            logger.warning(f"URL shortener check error: {e}")
            return False
    
    @staticmethod
    def count_special_characters(url: str) -> int:
        """
        Count special characters in URL
        
        Args:
            url: URL string
            
        Returns:
            Number of special characters
        """
        special_chars = r"[!@#$%^&*()_+=\[\]{};:'\"<>,.?/\\|`~]"
        return len(re.findall(special_chars, url))
