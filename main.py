from flask import Flask, jsonify
from dotenv import load_dotenv
from extensions import db, jwt, migrate
from auth import auth_bp
from users import user_bp
from jwt_handlers import register_jwt_handlers
from jwt_callbacks import check_if_token_revoked
import os

# Cargar variables de entorno con manejo de codificación
load_dotenv(encoding='latin-1')  # o 'utf-8-sig' si el archivo tiene BOM

def create_app():
    # Create and configure the Flask application
    app = Flask(__name__)
    
    # Load configuration from environment variables
    app.config.from_prefixed_env()
    
    # Set default configuration for microservice
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('FLASK_JWT_SECRET_KEY'),
        JWT_ACCESS_TOKEN_EXPIRES=3600,  # 1 hour
        JWT_REFRESH_TOKEN_EXPIRES=30*24*3600,  # 30 days
        JWT_TOKEN_LOCATION=["headers"],
        JWT_HEADER_NAME="Authorization",
        JWT_HEADER_TYPE="Bearer",
        JWT_ERROR_MESSAGE_KEY="error",
        JWT_BLOCKLIST_ENABLED=True,
        JWT_BLOCKLIST_TOKEN_CHECKS=["access", "refresh"]
    )
    
    # Initialize the database
    db.init_app(app)
    
    # Initialize migrations
    migrate.init_app(app, db)
    
    # Initialize JWT manager
    jwt.init_app(app)
    
    # Register JWT callbacks
    jwt.token_in_blocklist_loader(check_if_token_revoked)
    
    # register blueprints
    app.register_blueprint(
        auth_bp,
        url_prefix='/auth'
    )
    
    app.register_blueprint(
        user_bp,
        url_prefix='/users'
    )
    
    # Register JWT handlers
    register_jwt_handlers(jwt)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'auth-service'
        })
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'service': 'auth-service',
            'version': '1.0.0',
            'status': 'running'
        })
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)