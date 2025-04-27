from abc import ABC, abstractmethod
from typing import List, Optional
from backend.dao.users.user_class import User

class IUserDAO(ABC):
    """Interface for User Data Access Object"""
    
    @abstractmethod
    def get_all(self) -> List[User]:
        """
        Get all users
        
        Returns:
            List of User objects
        """
        pass
        
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object if found, None otherwise
        """
        pass
        
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username
        
        Args:
            username: Username
            
        Returns:
            User object if found, None otherwise
        """
        pass
        
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            email: Email address
            
        Returns:
            User object if found, None otherwise
        """
        pass
        
    @abstractmethod
    def create(self, username: str, email: str, password: str) -> int:
        """
        Create new user
        
        Args:
            username: Username
            email: Email address
            password: Password
            
        Returns:
            ID of created user
        """
        pass
        
    @abstractmethod
    def update(self, user_id: int, data: dict) -> bool:
        """
        Update user
        
        Args:
            user_id: User ID
            data: Dictionary containing fields to update
            
        Returns:
            True if update successful, False otherwise
        """
        pass
        
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Delete user
        
        Args:
            user_id: User ID
            
        Returns:
            True if deletion successful, False otherwise
        """
        pass 