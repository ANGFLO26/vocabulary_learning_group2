from flask import Blueprint, request, jsonify
from backend.business_layer.services.user_service import UserService
from backend.business_layer.services.topic_service import TopicService
from backend.business_layer.services.vocabulary_service import VocabularyService
from backend.business_layer.services.test_service import TestService
from backend.business_layer.services.test_result_service import TestResultService
from backend.business_layer.services.leaderboard_service import LeaderboardService
from backend.dao.users.user_dao import UserDAO
from backend.dao.topics.topic_dao import TopicDAO
from backend.utils.auth import token_required, get_current_user_id
from backend.utils.exceptions import (
    ValidationError, AuthenticationError, AuthorizationError,
    ResourceNotFoundError, DatabaseError, ServiceError
)
from backend.utils.validation import (
    validate_required_fields, validate_string_length,
    validate_email, validate_password, validate_integer,
    validate_integer_range, validate_float_range
)
from backend.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

learning_bp = Blueprint('learning', __name__)

# Error handlers
@learning_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    logger.warning(f"Validation error: {str(error)}")
    return jsonify({'error': str(error)}), 400

@learning_bp.errorhandler(AuthenticationError)
def handle_authentication_error(error):
    logger.warning(f"Authentication error: {str(error)}")
    return jsonify({'error': str(error)}), 401

@learning_bp.errorhandler(AuthorizationError)
def handle_authorization_error(error):
    logger.warning(f"Authorization error: {str(error)}")
    return jsonify({'error': str(error)}), 403

@learning_bp.errorhandler(ResourceNotFoundError)
def handle_not_found_error(error):
    logger.warning(f"Resource not found: {str(error)}")
    return jsonify({'error': str(error)}), 404

@learning_bp.errorhandler(DatabaseError)
def handle_database_error(error):
    logger.error(f"Database error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@learning_bp.errorhandler(ServiceError)
def handle_service_error(error):
    logger.error(f"Service error: {str(error)}")
    return jsonify({'error': str(error)}), 500

@learning_bp.errorhandler(Exception)
def handle_generic_error(error):
    logger.error(f"Unexpected error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# User APIs
@learning_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("No data provided")

        # Validate required fields
        errors = validate_required_fields(data, ['username', 'password', 'email'])
        if errors:
            raise ValidationError(errors[0])
        
        username = data['username']
        password = data['password']
        email = data['email']
        
        # Validate field formats
        username_error = validate_string_length(username, 'username', min_length=3)
        if username_error:
            raise ValidationError(username_error)
            
        password_error = validate_password(password)
        if password_error:
            raise ValidationError(password_error)
            
        email_error = validate_email(email)
        if email_error:
            raise ValidationError(email_error)
        
        # Initialize services
        user_dao = UserDAO()
        user_service = UserService(user_dao)
        
        # Try to register
        user = user_service.register(username, password, email)
        if not user:
            raise ServiceError('Username already exists')
            
        logger.info(f"User registered successfully: {username}")
        return jsonify(user.to_dict()), 201
        
    except ValidationError as e:
        logger.warning(f"Registration validation failed: {str(e)}")
        raise
    except ServiceError as e:
        logger.error(f"Registration service error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Registration failed with unexpected error: {str(e)}")
        raise

@learning_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        validate_required_fields(data, ['username', 'password'])
        
        username = data['username']
        password = data['password']
        
        user_dao = UserDAO()
        user_service = UserService(user_dao)
        result = user_service.login(username, password)
        
        if not result:
            raise AuthenticationError('Invalid credentials')
            
        logger.info(f"User logged in successfully: {username}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise

# Topic APIs
@learning_bp.route('/topics', methods=['GET'])
@token_required
def get_topics():
    try:
        topic_service = TopicService(TopicDAO())
        topics = topic_service.get_all_topics()
        return jsonify([topic.to_dict() for topic in topics]), 200
    except Exception as e:
        logger.error(f"Failed to get topics: {str(e)}")
        raise

@learning_bp.route('/topics/<int:topic_id>', methods=['GET'])
@token_required
def get_topic(topic_id):
    topic_service = TopicService(TopicDAO())
    topic = topic_service.get_topic_by_id(topic_id)
    
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
        
    return jsonify(topic.to_dict()), 200

# Vocabulary APIs
@learning_bp.route('/topics/<int:topic_id>/vocabularies', methods=['GET'])
@token_required
def get_vocabularies(topic_id):
    try:
        validate_integer(topic_id, 'topic_id', min_value=1)
        vocabulary_service = VocabularyService()
        vocabularies = vocabulary_service.get_vocabularies_by_topic(topic_id)
        return jsonify([vocabulary.to_dict() for vocabulary in vocabularies]), 200
    except Exception as e:
        logger.error(f"Failed to get vocabularies: {str(e)}")
        raise

@learning_bp.route('/vocabularies/<int:vocabulary_id>', methods=['GET'])
@token_required
def get_vocabulary(vocabulary_id):
    vocabulary_service = VocabularyService()
    vocabulary = vocabulary_service.get_vocabulary_by_id(vocabulary_id)
    
    if not vocabulary:
        return jsonify({'error': 'Vocabulary not found'}), 404
        
    return jsonify(vocabulary.to_dict()), 200

# Test APIs
@learning_bp.route('/topics/<int:topic_id>/tests', methods=['GET'])
@token_required
def get_tests(topic_id):
    test_service = TestService()
    tests = test_service.get_tests_by_topic(topic_id)
    return jsonify([test.to_dict() for test in tests]), 200

@learning_bp.route('/tests/<int:test_id>', methods=['GET'])
@token_required
def get_test(test_id):
    test_service = TestService()
    test = test_service.get_test_by_id(test_id)
    
    if not test:
        return jsonify({'error': 'Test not found'}), 404
        
    return jsonify(test.to_dict()), 200

# Test submission
@learning_bp.route('/tests/submit', methods=['POST'])
@token_required
def submit_test():
    user_id = get_current_user_id()
    data = request.get_json()
    topic_id = data.get('topic_id')
    answers = data.get('answers')
    completion_time = data.get('completion_time')
    
    if not all([topic_id, answers, completion_time]):
        return jsonify({'error': 'Missing required fields'}), 400
        
    test_service = TestService()
    result = test_service.submit_test_result(user_id, topic_id, answers, completion_time)
    
    if 'error' in result:
        return jsonify(result), 400
        
    return jsonify(result), 200

# Test Result APIs
@learning_bp.route('/user/results', methods=['GET'])
@token_required
def get_user_results():
    user_id = get_current_user_id()
    test_result_service = TestResultService()
    results = test_result_service.get_user_results(user_id)
    return jsonify([result.to_dict() for result in results]), 200

@learning_bp.route('/topics/<int:topic_id>/results', methods=['GET'])
@token_required
def get_topic_results(topic_id):
    test_result_service = TestResultService()
    results = test_result_service.get_topic_results(topic_id)
    return jsonify([result.to_dict() for result in results]), 200

@learning_bp.route('/user/topics/<int:topic_id>/results', methods=['GET'])
@token_required
def get_user_topic_results(topic_id):
    user_id = get_current_user_id()
    test_result_service = TestResultService()
    results = test_result_service.get_user_topic_results(user_id, topic_id)
    return jsonify([result.to_dict() for result in results]), 200

# Leaderboard APIs
@learning_bp.route('/topics/<int:topic_id>/leaderboard', methods=['GET'])
@token_required
def get_topic_leaderboard(topic_id):
    leaderboard_service = LeaderboardService()
    leaderboard = leaderboard_service.get_topic_leaderboard(topic_id)
    return jsonify([entry.to_dict() for entry in leaderboard]), 200

@learning_bp.route('/user/rank/<int:topic_id>', methods=['GET'])
@token_required
def get_user_rank(topic_id):
    user_id = get_current_user_id()
    leaderboard_service = LeaderboardService()
    rank = leaderboard_service.get_user_rank(user_id, topic_id)
    
    if not rank:
        return jsonify({'error': 'User not found in leaderboard'}), 404
        
    return jsonify({'rank': rank}), 200

@learning_bp.route('/topics/<int:topic_id>/top-users', methods=['GET'])
@token_required
def get_top_users(topic_id):
    limit = request.args.get('limit', default=10, type=int)
    leaderboard_service = LeaderboardService()
    top_users = leaderboard_service.get_top_users(topic_id, limit)
    return jsonify([user.to_dict() for user in top_users]), 200

# Statistics APIs
@learning_bp.route('/user/statistics', methods=['GET'])
@token_required
def get_user_statistics():
    user_id = get_current_user_id()
    test_result_service = TestResultService()
    leaderboard_service = LeaderboardService()
    
    test_stats = test_result_service.get_user_statistics(user_id)
    leaderboard_stats = leaderboard_service.get_user_statistics(user_id)
    
    return jsonify({
        'test_statistics': test_stats,
        'leaderboard_statistics': leaderboard_stats
    }), 200

@learning_bp.route('/topics/<int:topic_id>/statistics', methods=['GET'])
@token_required
def get_topic_statistics(topic_id):
    test_result_service = TestResultService()
    leaderboard_service = LeaderboardService()
    
    test_stats = test_result_service.get_topic_statistics(topic_id)
    leaderboard_stats = leaderboard_service.get_topic_statistics(topic_id)
    
    return jsonify({
        'test_statistics': test_stats,
        'leaderboard_statistics': leaderboard_stats
    }), 200 