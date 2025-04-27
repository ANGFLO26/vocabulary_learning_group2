import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from backend.config.config import JWT_CONFIG
from backend.dao.users.user_dao import UserDAO
from backend.dao.users.user_class import User
from backend.utils.exceptions import AuthenticationError, ValidationError

class AuthService:
    """Service for handling authentication operations"""
    
    def __init__(self):
        self.user_dao = UserDAO()
        
    def register_user(self, username: str, email: str, password: str) -> User:
        """
        Register a new user
        
        Args:
            username: Username
            email: Email address
            password: Password
            
        Returns:
            Created user object
            
        Raises:
            ValidationError: If username or email already exists
        """
        # Check if username exists
        if self.user_dao.get_by_username(username):
            raise ValidationError("Username already exists")
            
        # Check if email exists
        if self.user_dao.get_by_email(email):
            raise ValidationError("Email already exists")
            
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Create user
        user_id = self.user_dao.create(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8')
        )
        
        return self.user_dao.get_by_id(user_id)
        
    def login_user(self, username: str, password: str) -> str:
        """
        Login user and return JWT token
        
        Args:
            username: Username
            password: Password
            
        Returns:
            JWT token
            
        Raises:
            AuthenticationError: If credentials are invalid
        """
        # Get user
        user = self.user_dao.get_by_username(username)
        if not user:
            raise AuthenticationError("Invalid username or password")
            
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise AuthenticationError("Invalid username or password")
            
        # Generate token
        token = self._generate_token(user)
        
        return token
        
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token and return user data
        
        Args:
            token: JWT token
            
        Returns:
            User data if token is valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                JWT_CONFIG['secret_key'],
                algorithms=[JWT_CONFIG['algorithm']]
            )
            
            # Check if token has expired
            exp = datetime.fromtimestamp(payload['exp'])
            if exp < datetime.utcnow():
                return None
                
            return payload
            
        except jwt.InvalidTokenError:
            return None
            
    def _generate_token(self, user: User) -> str:
        """
        Generate JWT token for user
        
        Args:
            user: User object
            
        Returns:
            JWT token
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(minutes=JWT_CONFIG['access_token_expire_minutes'])
        }
        
        token = jwt.encode(
            payload,
            JWT_CONFIG['secret_key'],
            algorithm=JWT_CONFIG['algorithm']
        )
        
        return token 