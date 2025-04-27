from flask import Blueprint, request, jsonify
from backend.business_layer.auth_service import AuthService
from backend.utils.validation import validate_registration_data, validate_login_data
from backend.utils.exceptions import ValidationError, AuthenticationError, DatabaseError
from backend.utils.logger import logger
from functools import wraps

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                raise AuthenticationError('Token is missing')
            
            token = token.split(' ')[1] if len(token.split(' ')) > 1 else token
            user = auth_service.verify_token(token)
            if not user:
                raise AuthenticationError('Invalid token')
            
            return f(user, *args, **kwargs)
            
        except AuthenticationError as e:
            logger.warning(f"Authentication failed: {str(e)}")
            return jsonify({'error': str(e)}), 401
            
        except Exception as e:
            logger.error(f"Unexpected error in token validation: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
            
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError('No data provided')
            
        # Validate input data
        errors = validate_registration_data(data)
        if errors:
            raise ValidationError({'errors': errors})
            
        # Register user
        user = auth_service.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        logger.info(f"User registered successfully: {user.username}")
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Registration validation failed: {str(e)}")
        return jsonify({'error': str(e)}), 400
        
    except DatabaseError as e:
        logger.error(f"Database error during registration: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500
        
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError('No data provided')
            
        # Validate input data
        errors = validate_login_data(data)
        if errors:
            raise ValidationError({'errors': errors})
            
        # Login user
        token = auth_service.login_user(
            username=data['username'],
            password=data['password']
        )
        
        logger.info(f"User logged in successfully: {data['username']}")
        return jsonify({
            'message': 'Login successful',
            'token': token
        }), 200
        
    except ValidationError as e:
        logger.warning(f"Login validation failed: {str(e)}")
        return jsonify({'error': str(e)}), 400
        
    except AuthenticationError as e:
        logger.warning(f"Login authentication failed: {str(e)}")
        return jsonify({'error': str(e)}), 401
        
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 