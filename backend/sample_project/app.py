"""
Main application entry point.
"""
from config import Config
from core.router import Router
from core.logger import Logger
from services.auth import AuthService
from services.database import DatabaseService
from models.user import User
from models.product import Product

logger = Logger(__name__)
config = Config()

def main():
    """Initialize and run the application."""
    logger.info("Starting application...")
    
    # Initialize services
    db_service = DatabaseService(config)
    auth_service = AuthService(db_service)
    router = Router(auth_service)
    
    # Create sample user
    user = User("john_doe", "john@example.com")
    logger.info(f"Created user: {user.username}")
    
    # Create sample product
    product = Product("Laptop", 999.99)
    logger.info(f"Created product: {product.name}")
    
    # Process request
    router.handle_request("/api/users", user)
    
    logger.info("Application started successfully")

if __name__ == "__main__":
    main()

