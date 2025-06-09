from flask import jsonify
from models import User

def register_jwt_handlers(jwt):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'message': 'token ha expirado',
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'message': 'verificacion del token invalido',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'message': 'token no proporcionado',
            'error': 'missing_token'
        }), 401

    
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        
        if identity == "admin":
            return {'is_admin': True}
        return {'is_admin': False}
    
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()