"""
Old API implementation - no longer used.
This module is never imported anywhere.
"""
from datetime import datetime

class OldAPI:
    """Deprecated API class."""
    
    def __init__(self):
        self.version = "1.0"
        print("Old API initialized (this should never be called)")
    
    def process_request(self, data: dict):
        """Process API request - deprecated method."""
        print(f"Processing request with old API: {data}")
        return {"status": "deprecated", "timestamp": datetime.now()}
    
    def get_status(self):
        """Get API status."""
        return {"version": self.version, "status": "deprecated"}

def legacy_function():
    """Legacy function that is never called."""
    print("This function is never called")
    return "legacy"

