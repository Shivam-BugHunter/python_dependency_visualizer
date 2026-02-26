"""
Unused math utilities - never imported.
This module contains functions that are never used.
"""
import math

def calculate_fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number - never used."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

def calculate_prime(n: int) -> bool:
    """Check if number is prime - never used."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def complex_calculation(x: float, y: float) -> float:
    """Perform complex calculation - never used."""
    result = math.sin(x) * math.cos(y) + math.sqrt(x * y)
    print(f"Complex calculation result: {result}")
    return result

class MathHelper:
    """Helper class for math operations - never used."""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial."""
        if n <= 1:
            return 1
        return n * MathHelper.factorial(n - 1)
    
    @staticmethod
    def power(base: float, exponent: float) -> float:
        """Calculate power."""
        return math.pow(base, exponent)

