"""
Utility functions for the application.
"""
import hashlib
import json
from datetime import datetime
from core.logger import Logger

logger = Logger(__name__)

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    logger.debug("Hashing password")
    return hashlib.sha256(password.encode()).hexdigest()

def format_date(date: datetime) -> str:
    """Format a datetime object as a string."""
    return date.strftime("%Y-%m-%d %H:%M:%S")

def parse_json(data: str) -> dict:
    """Parse JSON string to dictionary."""
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return {}

def validate_email(email: str) -> bool:
    """Validate email format."""
    return "@" in email and "." in email.split("@")[1]

def calculate_total(items: list) -> float:
    """Calculate total from a list of items with price attribute."""
    total = sum(item.get("price", 0) for item in items)
    logger.info(f"Calculated total: {total}")
    return total
