# PhishGuard - Logging Configuration
# Centralized logging setup for the application

import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import get_settings


def setup_logging():
    """Configure logging for the application"""
    settings = get_settings()
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Get logger
    logger = logging.getLogger("phishguard")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# Initialize logger
logger = setup_logging()
