from abc import ABC, abstractmethod
from typing import Optional, Dict
from backend.dao.users.user_class import User

class IUserService(ABC):
    """Interface for User Service"""
    
    @abstractmethod
    def register(self, username: str, password: str, email: str) -> Optional[User]:
        """Register a new user"""
        pass
        
    @abstractmethod
    def login(self, username: str, password: str) -> Optional[Dict]:
        """Login user and return token"""
        pass
        
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
        
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
        
    @abstractmethod
    def update_user(self, user_id: int, username: str, email: str) -> bool:
        """Update user information"""
        pass
        
    @abstractmethod
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        pass 