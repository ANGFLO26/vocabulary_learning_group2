from flask import Flask
from flask_cors import CORS
from backend.api.auth import auth_bp
from backend.api.learning import learning_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(learning_bp, url_prefix='/api/learning')
    
    return app 

# This file makes the directory a Python package 