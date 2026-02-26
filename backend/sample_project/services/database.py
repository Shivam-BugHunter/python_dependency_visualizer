"""
Database service for data persistence.
"""
from config import Config
from core.logger import Logger
from core.cache import Cache

logger = Logger(__name__)

class DatabaseService:
    """Handles database operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self.cache = Cache()
        self._users = {}
        self._orders = {}
        self._payments = {}
        logger.info("DatabaseService initialized")
    
    def get_user(self, username: str) -> dict:
        """Retrieve user from database."""
        cache_key = f"user:{username}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.debug(f"User {username} retrieved from cache")
            return cached
        
        user_data = self._users.get(username)
        if user_data:
            self.cache.set(cache_key, user_data)
        
        logger.debug(f"User {username} retrieved from database")
        return user_data
    
    def save_user(self, user, password_hash: str):
        """Save user to database."""
        self._users[user.username] = {
            "username": user.username,
            "email": user.email,
            "password": password_hash
        }
        logger.info(f"User {user.username} saved to database")
    
    def get_order_items(self, order_id: str) -> list:
        """Retrieve order items."""
        order = self._orders.get(order_id)
        if order:
            return order.get("items", [])
        return []
    
    def save_payment(self, order_id: str, amount: float) -> str:
        """Save payment record."""
        payment_id = f"pay_{order_id}_{len(self._payments)}"
        self._payments[payment_id] = {
            "order_id": order_id,
            "amount": amount,
            "status": "completed"
        }
        logger.info(f"Payment {payment_id} saved")
        return payment_id
    
    def get_payment(self, payment_id: str) -> dict:
        """Retrieve payment record."""
        return self._payments.get(payment_id)

