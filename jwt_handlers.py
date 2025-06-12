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

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'message': 'token ha sido revocado',
            'error': 'token_revoked'
        }), 401
    
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user = User.query.get(identity)
        if user is None:
            return {'roles': []}
            
        # Obtener los nombres de los roles del usuario
        roles = [role.name for role in user.roles]
        
        return {
            'roles': roles,
            'username': user.username,
            'email': user.email
        }
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()