from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserEntity:
    """Entity representing a user in the database"""
    
    id: Optional[int]
    username: str
    email: str
    password: str
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_db_row(row: tuple) -> 'UserEntity':
        """
        Create UserEntity from database row
        
        Args:
            row: Database row tuple (id, username, email, password, created_at)
            
        Returns:
            UserEntity object
        """
        return UserEntity(
            id=row[0],
            username=row[1],
            email=row[2],
            password=row[3],
            created_at=row[4]
        )
        
    def to_db_tuple(self) -> tuple:
        """Convert to database tuple for insertion/update"""
        return (
            self.username,
            self.email,
            self.password,
            self.created_at
        ) 