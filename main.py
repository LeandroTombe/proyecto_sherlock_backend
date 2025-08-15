from flask import Flask, jsonify
from dotenv import load_dotenv
from src.config.extensions import db, jwt, migrate
from src.api.auth_routes import auth_bp
from src.api.jwt_handlers import register_jwt_handlers
import os

# Cargar variables de entorno
load_dotenv(encoding='latin-1')

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config.from_prefixed_env()
    
    # Configuración de base de datos
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Configuración por defecto para desarrollo local
        database_url = "postgresql://postgres:postgres@localhost:5432/auth_db_local"
    
    app.config.update(
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('FLASK_JWT_SECRET_KEY', 'tu_clave_secreta_super_segura_local'),
        JWT_ACCESS_TOKEN_EXPIRES=3600,  # 1 hour
        JWT_REFRESH_TOKEN_EXPIRES=30*24*3600,  # 30 days
        JWT_TOKEN_LOCATION=["headers"],
        JWT_HEADER_NAME="Authorization",
        JWT_HEADER_TYPE="Bearer",
        JWT_ERROR_MESSAGE_KEY="error",
        JWT_BLOCKLIST_ENABLED=True,
        JWT_BLOCKLIST_TOKEN_CHECKS=["access", "refresh"]
    )
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Registrar manejadores JWT
    register_jwt_handlers(jwt)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
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