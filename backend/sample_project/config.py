"""
Application configuration management.
"""
import os
from core.logger import Logger

logger = Logger(__name__)

class Config:
    """Application configuration."""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://localhost:5432/mydb")
        self.secret_key = os.getenv("SECRET_KEY", "default-secret-key")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.api_timeout = int(os.getenv("API_TIMEOUT", "30"))
        
        logger.info("Configuration loaded")
    
    def get_database_url(self):
        """Get database connection URL."""
        return self.database_url
    
    def get_secret_key(self):
        """Get secret key for encryption."""
        return self.secret_key
    
    def is_debug(self):
        """Check if debug mode is enabled."""
        return self.debug

