import logging
import logging.handlers
import os
from typing import Optional
from datetime import datetime

from backend.config import LOG_CONFIG

def setup_logger(name: str, log_file: Optional[str] = None,
                level: str = LOG_CONFIG['level']) -> logging.Logger:
    """Sets up a logger with console and file handlers."""
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log file is specified
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_function_call(logger: logging.Logger, func_name: str, args: tuple,
                     kwargs: dict) -> None:
    """Logs function call with arguments."""
    args_str = ', '.join([str(arg) for arg in args])
    kwargs_str = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
    params = f"{args_str}{', ' if args_str and kwargs_str else ''}{kwargs_str}"
    logger.debug(f"Calling {func_name}({params})")

def log_function_result(logger: logging.Logger, func_name: str,
                       result: any) -> None:
    """Logs function result."""
    logger.debug(f"{func_name} returned: {result}")

def log_exception(logger: logging.Logger, exc: Exception,
                 context: Optional[str] = None) -> None:
    """Logs exception with context."""
    message = f"Exception occurred"
    if context:
        message = f"{message} in {context}"
    logger.exception(message, exc_info=exc)

def log_api_request(logger: logging.Logger, method: str, path: str,
                   params: dict, body: dict) -> None:
    """Logs API request details."""
    logger.info(f"API Request: {method} {path}")
    logger.debug(f"Parameters: {params}")
    logger.debug(f"Body: {body}")

def log_api_response(logger: logging.Logger, status_code: int,
                    response_body: dict, duration: float) -> None:
    """Logs API response details."""
    logger.info(f"API Response: {status_code} (took {duration:.2f}s)")
    logger.debug(f"Response body: {response_body}")

def log_database_query(logger: logging.Logger, query: str,
                      params: tuple) -> None:
    """Logs database query with parameters."""
    logger.debug(f"Executing query: {query}")
    logger.debug(f"Parameters: {params}")

def log_authentication(logger: logging.Logger, user_id: int,
                      action: str) -> None:
    """Logs authentication events."""
    logger.info(f"User {user_id}: {action}")

def log_error(logger: logging.Logger, message: str,
              error_code: Optional[str] = None) -> None:
    """Logs error with optional error code."""
    if error_code:
        logger.error(f"[{error_code}] {message}")
    else:
        logger.error(message)

# Create and export loggers
logger = setup_logger('vocabulary_app', LOG_CONFIG.get('file'))
api_logger = setup_logger('vocabulary_app.api')
db_logger = setup_logger('vocabulary_app.database')
auth_logger = setup_logger('vocabulary_app.auth')

__all__ = ['logger', 'api_logger', 'db_logger', 'auth_logger',
           'log_function_call', 'log_function_result', 'log_exception',
           'log_api_request', 'log_api_response', 'log_database_query',
           'log_authentication', 'log_error', 'setup_logger'] 