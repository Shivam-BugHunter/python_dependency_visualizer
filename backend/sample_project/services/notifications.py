"""
Notification service.
"""
from services.auth import AuthService
from core.logger import Logger
from utils import format_date
from datetime import datetime

logger = Logger(__name__)

class NotificationService:
    """Handles sending notifications."""
    
    def __init__(self):
        logger.info("NotificationService initialized")
    
    def send_login_notification(self, username: str):
        """Send login notification."""
        timestamp = format_date(datetime.now())
        message = f"User {username} logged in at {timestamp}"
        logger.info(f"Sending notification: {message}")
        print(f"📧 Notification: {message}")
    
    def send_welcome_notification(self, username: str, email: str):
        """Send welcome notification to new user."""
        message = f"Welcome {username}! Your account has been created."
        logger.info(f"Sending welcome notification to {email}")
        print(f"📧 Welcome email sent to {email}: {message}")
    
    def send_logout_notification(self, username: str):
        """Send logout notification."""
        timestamp = format_date(datetime.now())
        message = f"User {username} logged out at {timestamp}"
        logger.info(f"Sending notification: {message}")
        print(f"📧 Notification: {message}")
    
    def send_order_notification(self, order_id: str, user_email: str):
        """Send order confirmation notification."""
        message = f"Your order {order_id} has been confirmed."
        logger.info(f"Sending order notification to {user_email}")
        print(f"📧 Order confirmation sent to {user_email}: {message}")

