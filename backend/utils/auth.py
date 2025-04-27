from functools import wraps
from typing import Optional, Callable
import jwt
from flask import request, jsonify, g
from datetime import datetime, timedelta

from backend.config import JWT_CONFIG
from backend.utils.exceptions import AuthenticationError, AuthorizationError

def generate_token(user_id: int) -> str:
    """Generates a JWT token for the given user ID."""
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(minutes=JWT_CONFIG['access_token_expire_minutes'])
        }
        return jwt.encode(payload, JWT_CONFIG['secret_key'], algorithm=JWT_CONFIG['algorithm'])
    except Exception as e:
        raise AuthenticationError(f"Error generating token: {str(e)}")

def decode_token(token: str) -> dict:
    """Decodes and validates a JWT token."""
    try:
        return jwt.decode(token, JWT_CONFIG['secret_key'], algorithms=[JWT_CONFIG['algorithm']])
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")

def get_token_from_header() -> str:
    """Extracts the token from the Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthenticationError("No Authorization header")
        
    parts = auth_header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        raise AuthenticationError("Invalid Authorization header format")
        
    return parts[1]

def token_required(f: Callable) -> Callable:
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Get token from header
            token = get_token_from_header()
            
            # Decode and validate token
            payload = decode_token(token)
            
            # Store user_id in Flask's g object for route handlers
            g.user_id = payload['user_id']
            
            return f(*args, **kwargs)
        except AuthenticationError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
            
    return decorated

def get_current_user_id() -> int:
    """Gets the current authenticated user's ID from Flask's g object."""
    user_id = getattr(g, 'user_id', None)
    if user_id is None:
        raise AuthorizationError("No authenticated user found")
    return user_id

def admin_required(f: Callable) -> Callable:
    """Decorator to protect routes that require admin privileges."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # First check if user is authenticated
            token = get_token_from_header()
            payload = decode_token(token)
            
            # Check if user has admin role (you would need to implement this check)
            if not is_admin(payload['user_id']):
                raise AuthorizationError("Admin privileges required")
                
            g.user_id = payload['user_id']
            return f(*args, **kwargs)
        except (AuthenticationError, AuthorizationError) as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
            
    return decorated

def is_admin(user_id: int) -> bool:
    """Checks if a user has admin privileges.
    This is a placeholder - you should implement the actual check based on your user roles system.
    """
    # TODO: Implement actual admin check
    return False  # For now, no one is admin

def verify_user_access(resource_user_id: int) -> bool:
    """Verifies that the current user has access to a user-specific resource."""
    current_user_id = get_current_user_id()
    return current_user_id == resource_user_id or is_admin(current_user_id) 