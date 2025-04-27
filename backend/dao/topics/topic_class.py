from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class Topic:
    """Class representing a topic in the system"""
    
    id: Optional[int]
    name: str
    description: str
    created_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
    def validate(self) -> bool:
        """Validate topic data"""
        if not self.name or len(self.name) > 255:
            return False
            
        if not self.description or len(self.description) > 1000:
            return False
            
        return True
        
    def to_dict(self) -> Dict:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at
        } 