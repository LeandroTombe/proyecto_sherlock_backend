from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt = get_jwt()
            if "roles" not in jwt:
                return jsonify({"error": "No roles found in token"}), 403
                
            if not any(role in jwt["roles"] for role in roles):
                return jsonify({"error": "Insufficient permissions"}), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper 