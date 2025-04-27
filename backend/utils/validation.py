from typing import Dict, Any, List, Optional
from backend.utils.exceptions import ValidationError
import re

def validate_required_fields(data: Dict[str, Any], fields: List[str]) -> List[str]:
    """Validates that all required fields are present and not empty."""
    missing_fields = []
    for field in fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
            
    return [f"Missing required fields: {', '.join(missing_fields)}"] if missing_fields else []

def validate_integer(value: Any, field: str, min_value: Optional[int] = None,
                    max_value: Optional[int] = None) -> Optional[str]:
    """Validates that a value is an integer and optionally within a range."""
    try:
        int_value = int(value)
    except (TypeError, ValueError):
        return f"{field} must be an integer"
        
    if min_value is not None and int_value < min_value:
        return f"{field} must be greater than or equal to {min_value}"
        
    if max_value is not None and int_value > max_value:
        return f"{field} must be less than or equal to {max_value}"
        
    return None

def validate_string_length(value: str, field: str, min_length: int = 1, max_length: int = 255) -> Optional[str]:
    """Validates string length is within specified range."""
    if not min_length <= len(value) <= max_length:
        return f"{field} must be between {min_length} and {max_length} characters"
    return None

def validate_email(email: str) -> Optional[str]:
    """Validates email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return "Invalid email format"
    return None

def validate_password(password: str) -> Optional[str]:
    """Validates password strength."""
    if len(password) < 8:
        return "Password must be at least 8 characters long"
        
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter"
        
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter"
        
    if not re.search(r'\d', password):
        return "Password must contain at least one number"
        
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character"
        
    return None

def validate_integer_range(value: int, field: str, min_value: Optional[int] = None,
                         max_value: Optional[int] = None) -> Optional[str]:
    """Validates integer value is within specified range."""
    if min_value is not None and value < min_value:
        return f"{field} must be greater than or equal to {min_value}"
        
    if max_value is not None and value > max_value:
        return f"{field} must be less than or equal to {max_value}"
        
    return None

def validate_float_range(value: float, field: str, min_value: Optional[float] = None,
                        max_value: Optional[float] = None) -> Optional[str]:
    """Validates float value is within specified range."""
    if min_value is not None and value < min_value:
        return f"{field} must be greater than or equal to {min_value}"
        
    if max_value is not None and value > max_value:
        return f"{field} must be less than or equal to {max_value}"
        
    return None

def validate_list_length(value: List[Any], field: str, min_length: int = 0,
                        max_length: Optional[int] = None) -> Optional[str]:
    """Validates list length is within specified range."""
    if len(value) < min_length:
        return f"{field} must contain at least {min_length} items"
        
    if max_length is not None and len(value) > max_length:
        return f"{field} must contain at most {max_length} items"
        
    return None

def validate_username(username: str) -> Optional[str]:
    """Validates username format."""
    if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', username):
        return "Username must be 3-20 characters long and contain only letters, numbers, underscores, and hyphens"
    return None

def validate_date_format(date_str: str, field: str) -> Optional[str]:
    """Validates date string format (YYYY-MM-DD)."""
    try:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            raise ValueError
    except ValueError:
        return f"{field} must be in YYYY-MM-DD format"
    return None

def validate_time_format(time_str: str, field: str) -> Optional[str]:
    """Validates time string format (HH:MM:SS)."""
    try:
        if not re.match(r'^\d{2}:\d{2}:\d{2}$', time_str):
            raise ValueError
    except ValueError:
        return f"{field} must be in HH:MM:SS format"
    return None

def validate_registration_data(data: Dict) -> List[str]:
    """
    Validate user registration data
    
    Args:
        data: Registration data
        
    Returns:
        List of error messages
    """
    errors = []
    
    # Required fields
    errors.extend(validate_required_fields(data, ['username', 'email', 'password']))
    
    if not errors:
        # Username validation
        username_error = validate_username(data['username'])
        if username_error:
            errors.append(username_error)
            
        # Email validation
        email_error = validate_email(data['email'])
        if email_error:
            errors.append(email_error)
            
        # Password validation
        password_error = validate_password(data['password'])
        if password_error:
            errors.append(password_error)
            
    return errors

def validate_login_data(data: Dict) -> List[str]:
    """
    Validate user login data
    
    Args:
        data: Login data
        
    Returns:
        List of error messages
    """
    return validate_required_fields(data, ['username', 'password'])

__all__ = [
    'validate_required_fields',
    'validate_string_length',
    'validate_email',
    'validate_password',
    'validate_integer',
    'validate_integer_range',
    'validate_float_range',
    'validate_list_length',
    'validate_username',
    'validate_date_format',
    'validate_time_format',
    'validate_registration_data',
    'validate_login_data'
] 