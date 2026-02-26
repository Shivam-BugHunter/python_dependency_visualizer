"""
Product model.
"""
from core.logger import Logger
from utils import calculate_total

logger = Logger(__name__)

class Product:
    """Represents a product in the system."""
    
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        self.stock = 0
        logger.debug(f"Product instance created: {name}")
    
    def __str__(self):
        return f"Product(name={self.name}, price=${self.price})"
    
    def __repr__(self):
        return self.__str__()
    
    def get_info(self) -> dict:
        """Get product information."""
        return {
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }
    
    def update_price(self, new_price: float):
        """Update product price."""
        logger.info(f"Updating price for {self.name}: ${new_price}")
        self.price = new_price
    
    def calculate_discount(self, discount_percent: float) -> float:
        """Calculate discounted price."""
        discount_amount = self.price * (discount_percent / 100)
        discounted_price = self.price - discount_amount
        logger.debug(f"Discount calculated: ${discounted_price}")
        return discounted_price

