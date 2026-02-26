"""
Payment processing service.
"""
from services.database import DatabaseService
from models.order import Order
from core.logger import Logger
from utils import calculate_total

logger = Logger(__name__)

class PaymentService:
    """Handles payment processing."""
    
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        logger.info("PaymentService initialized")
    
    def process_payment(self, order: Order, amount: float) -> bool:
        """Process a payment for an order."""
        logger.info(f"Processing payment for order {order.order_id}: ${amount}")
        
        if amount <= 0:
            logger.error("Invalid payment amount")
            return False
        
        items = self.db_service.get_order_items(order.order_id)
        total = calculate_total(items)
        
        if amount < total:
            logger.warning(f"Insufficient payment: ${amount} < ${total}")
            return False
        
        # Simulate payment processing
        payment_id = self.db_service.save_payment(order.order_id, amount)
        logger.info(f"Payment processed successfully: {payment_id}")
        return True
    
    def refund_payment(self, payment_id: str) -> bool:
        """Process a refund."""
        logger.info(f"Processing refund for payment: {payment_id}")
        
        payment_data = self.db_service.get_payment(payment_id)
        if not payment_data:
            logger.error(f"Payment not found: {payment_id}")
            return False
        
        logger.info(f"Refund processed for payment: {payment_id}")
        return True

