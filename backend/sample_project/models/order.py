"""
Order model.
"""
import uuid
from core.logger import Logger
from models.product import Product
from utils import calculate_total

logger = Logger(__name__)

class Order:
    """Represents an order in the system."""
    
    def __init__(self, user_id: str):
        self.order_id = str(uuid.uuid4())
        self.user_id = user_id
        self.items = []
        self.status = "pending"
        logger.debug(f"Order instance created: {self.order_id}")
    
    def __str__(self):
        return f"Order(id={self.order_id}, status={self.status})"
    
    def __repr__(self):
        return self.__str__()
    
    def add_item(self, product: Product, quantity: int = 1):
        """Add item to order."""
        item = {
            "product": product.name,
            "price": product.price,
            "quantity": quantity
        }
        self.items.append(item)
        logger.info(f"Added item to order {self.order_id}: {product.name}")
    
    def get_total(self) -> float:
        """Calculate order total."""
        total = calculate_total(self.items)
        logger.debug(f"Order {self.order_id} total: ${total}")
        return total
    
    def complete(self):
        """Mark order as completed."""
        self.status = "completed"
        logger.info(f"Order {self.order_id} marked as completed")

