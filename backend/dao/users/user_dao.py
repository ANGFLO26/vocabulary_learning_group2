from typing import List, Optional
from datetime import datetime
from backend.database.database import get_db
from backend.config.config import TABLE_CONFIG
from .user_interface import IUserDAO
from .user_entity import UserEntity
from backend.dao.users.user_class import User
from backend.utils.exceptions import DatabaseError

class UserDAO(IUserDAO):
    """Implementation of User Data Access Object"""
    
    def __init__(self):
        self.db = get_db()
        self.table = TABLE_CONFIG['users']
        
    def get_all(self) -> List[User]:
        """Get all users"""
        try:
            cursor = self.db.cursor()
            cursor.execute(f"SELECT id, username, email, password, created_at FROM {self.table}")
            rows = cursor.fetchall()
            return [User(
                id=row[0],
                username=row[1], 
                email=row[2],
                password=row[3],
                created_at=row[4]
            ) for row in rows]
        except Exception as e:
            raise DatabaseError(f"Failed to get users: {str(e)}")
        
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                f"SELECT id, username, email, password, created_at FROM {self.table} WHERE id = %s",
                (user_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
                
            return User(
                id=row[0],
                username=row[1],
                email=row[2], 
                password=row[3],
                created_at=row[4]
            )
        except Exception as e:
            raise DatabaseError(f"Failed to get user: {str(e)}")
        
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                f"SELECT id, username, email, password, created_at FROM {self.table} WHERE username = %s",
                (username,)
            )
            row = cursor.fetchone()
            if not row:
                return None
                
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password=row[3],
                created_at=row[4]
            )
        except Exception as e:
            raise DatabaseError(f"Failed to get user: {str(e)}")
        
    def create(self, user: User) -> Optional[User]:
        """Create new user
        
        Args:
            user: User object to create
            
        Returns:
            Created user object with ID if successful, None otherwise
            
        Raises:
            DatabaseError: If database operation fails
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            
            # Insert user
            cursor.execute(
                f"INSERT INTO {self.table} (username, email, password, created_at) VALUES (%s, %s, %s, %s)",
                (user.username, user.email, user.password, user.created_at or datetime.now())
            )
            
            # Get inserted ID
            user_id = cursor.lastrowid
            
            # Commit transaction
            self.db.commit()
            
            # Return user with ID
            user.id = user_id
            return user
                
        except Exception as e:
            # Rollback on error
            if self.db:
                self.db.rollback()
            raise DatabaseError(f"Failed to create user: {str(e)}")
        finally:
            if cursor:
                cursor.close()
        
    def update(self, user: User) -> bool:
        """Update user
        
        Args:
            user: User object to update
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            DatabaseError: If database operation fails
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            
            # Update user
            cursor.execute(
                f"UPDATE {self.table} SET username = %s, email = %s, password = %s WHERE id = %s",
                (user.username, user.email, user.password, user.id)
            )
            
            # Commit transaction
            self.db.commit()
            
            return cursor.rowcount > 0
                
        except Exception as e:
            # Rollback on error
            if self.db:
                self.db.rollback()
            raise DatabaseError(f"Failed to update user: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        cursor = None
        try:
            cursor = self.db.cursor()
            
            cursor.execute(f"DELETE FROM {self.table} WHERE id = %s", (user_id,))
            
            # Commit transaction
            self.db.commit()
            
            return cursor.rowcount > 0
                
        except Exception as e:
            # Rollback on error
            if self.db:
                self.db.rollback()
            raise DatabaseError(f"Failed to delete user: {str(e)}")
        finally:
            if cursor:
                cursor.close()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                f"SELECT id, username, email, password, created_at FROM {self.table} WHERE email = %s",
                (email,)
            )
            row = cursor.fetchone()
            if not row:
                return None
                
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password=row[3],
                created_at=row[4]
            )
        except Exception as e:
            raise DatabaseError(f"Failed to get user: {str(e)}") 