class BaseError(Exception):
    """Base exception class for the application."""
    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)

class ValidationError(BaseError):
    """Raised when data validation fails."""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message)

class DatabaseError(BaseError):
    """Raised when database operations fail."""
    def __init__(self, message: str = "Database error"):
        super().__init__(message)

class AuthenticationError(BaseError):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)

class AuthorizationError(BaseError):
    """Raised when authorization fails."""
    def __init__(self, message: str = "Authorization failed"):
        super().__init__(message)

class ResourceNotFoundError(BaseError):
    """Raised when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)

class ResourceExistsError(BaseError):
    """Raised when attempting to create a resource that already exists."""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message)

class ServiceError(BaseError):
    """Raised when a service operation fails."""
    def __init__(self, message: str = "Service operation failed"):
        super().__init__(message)

class ConfigurationError(BaseError):
    """Raised when there is a configuration error."""
    def __init__(self, message: str = "Configuration error"):
        super().__init__(message)

class ExternalServiceError(BaseError):
    """Raised when an external service call fails."""
    def __init__(self, message: str = "External service error"):
        super().__init__(message) 