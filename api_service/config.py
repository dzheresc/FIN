"""
Configuration settings for the API service.
"""

import os
from typing import Optional


class Config:
    """Base configuration class."""
    
    # API Settings
    API_VERSION = "v1"
    API_PREFIX = "/api/v1"
    
    # Database Settings
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///risk_evaluations.db")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "risk_evaluations")
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    
    # Application Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    TESTING = False
    
    # CORS Settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", None)
    
    # File Storage Settings
    CSV_OUTPUT_DIR = os.getenv("CSV_OUTPUT_DIR", "./output")
    MAX_CSV_FILE_SIZE = int(os.getenv("MAX_CSV_FILE_SIZE", "10485760"))  # 10MB
    
    # Rate Limiting (if implemented)
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "False").lower() == "true"
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Currency Settings
    DEFAULT_BASE_CURRENCY = os.getenv("DEFAULT_BASE_CURRENCY", "USD")
    CURRENCY_RATES_API = os.getenv("CURRENCY_RATES_API", None)
    
    # Pagination Defaults
    DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "10"))
    MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "100"))


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///risk_evaluations_dev.db")


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")  # Must be set in production
    DATABASE_URL = os.getenv("DATABASE_URL")  # Must be set in production
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL must be set in production")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    DEBUG = True


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}


def get_config(config_name: Optional[str] = None) -> Config:
    """
    Get configuration class based on environment.
    
    Args:
        config_name: Configuration name (development, production, testing)
                    If None, uses FLASK_ENV environment variable
        
    Returns:
        Configuration class instance
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")
    
    return config.get(config_name, config["default"])

