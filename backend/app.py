from flask_jwt_extended import JWTManager
from backend.api import create_app
from backend.config import JWT_CONFIG, APP_CONFIG
from backend.utils.logger import logger

app = create_app()

# JWT Configuration
app.config['JWT_SECRET_KEY'] = JWT_CONFIG['secret_key']
app.config['JWT_ALGORITHM'] = JWT_CONFIG['algorithm']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_CONFIG['access_token_expire_minutes'] * 60  # Convert to seconds

# Initialize JWT
jwt = JWTManager(app)

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(
        debug=APP_CONFIG['debug'],
        host=APP_CONFIG['host'],
        port=APP_CONFIG['port']
    ) 