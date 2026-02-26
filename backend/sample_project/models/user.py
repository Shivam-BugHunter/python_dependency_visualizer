"""
User model.
"""
from core.logger import Logger

logger = Logger(__name__)

class User:
    """Represents a user in the system."""
    
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.created_at = None
        logger.debug(f"User instance created: {username}")
    
    def __str__(self):
        return f"User(username={self.username}, email={self.email})"
    
    def __repr__(self):
        return self.__str__()
    
    def get_profile(self) -> dict:
        """Get user profile information."""
        return {
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }
    
    def update_email(self, new_email: str):
        """Update user email."""
        logger.info(f"Updating email for {self.username}")
        self.email = new_email

