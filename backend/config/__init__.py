# This file makes the directory a Python package 

from .config import (
    DB_CONFIG,
    JWT_CONFIG,
    APP_CONFIG,
    LOG_CONFIG,
    TABLE_CONFIG,
    SQLALCHEMY_DATABASE_URL
)

# Export JWT secret key for convenience
SECRET_KEY = JWT_CONFIG['secret_key'] 