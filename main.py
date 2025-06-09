from flask import Flask, jsonify
from dotenv import load_dotenv
from extensions import db, jwt
from auth import auth_bp
from users import user_bp
from jwt_handlers import register_jwt_handlers
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
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/auth_db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('FLASK_JWT_SECRET_KEY', 'your-secret-key'),
        JWT_ACCESS_TOKEN_EXPIRES=3600,  # 1 hour
    )
    
    # Initialize the database
    db.init_app(app)
    
    # Initialize JWT manager
    jwt.init_app(app)
    
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