import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'database': 'vocabulary_learning'
}

# JWT configuration
JWT_CONFIG = {
    'secret_key': os.getenv('JWT_SECRET_KEY', 'your-secret-key'),
    'algorithm': os.getenv('JWT_ALGORITHM', 'HS256'),
    'access_token_expire_minutes': int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 30))
}

# Application configuration
APP_CONFIG = {
    'debug': os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
    'host': os.getenv('FLASK_HOST', '0.0.0.0'),
    'port': int(os.getenv('FLASK_PORT', 5000))
}

# Logging configuration
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'file': os.getenv('LOG_FILE', 'app.log')
}

# Database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345678@localhost/vocabulary_learning"

# Table names configuration
TABLE_CONFIG = {
    'users': 'users',
    'topics': 'vocabulary_topics',
    'vocabularies': 'vocabularies',
    'tests': 'tests',
    'test_results': 'test_results',
    'leaderboards': 'leaderboards'
} 