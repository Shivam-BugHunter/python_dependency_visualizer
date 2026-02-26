"""
Authentication service.
"""
from services.database import DatabaseService
from services.notifications import NotificationService
from models.user import User
from utils import hash_password, validate_email
from core.logger import Logger

logger = Logger(__name__)

class AuthService:
    """Handles user authentication."""
    
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        self.notification_service = NotificationService()
        logger.info("AuthService initialized")
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        logger.info(f"Attempting login for user: {username}")
        
        hashed_password = hash_password(password)
        user_data = self.db_service.get_user(username)
        
        if user_data and user_data.get("password") == hashed_password:
            self.notification_service.send_login_notification(username)
            logger.info(f"Login successful for user: {username}")
            return True
        
        logger.warning(f"Login failed for user: {username}")
        return False
    
    def register(self, username: str, email: str, password: str) -> User:
        """Register a new user."""
        logger.info(f"Registering new user: {username}")
        
        if not validate_email(email):
            raise ValueError("Invalid email format")
        
        hashed_password = hash_password(password)
        user = User(username, email)
        
        self.db_service.save_user(user, hashed_password)
        self.notification_service.send_welcome_notification(username, email)
        
        logger.info(f"User registered successfully: {username}")
        return user
    
    def logout(self, username: str):
        """Logout a user."""
        logger.info(f"Logging out user: {username}")
        self.notification_service.send_logout_notification(username)

