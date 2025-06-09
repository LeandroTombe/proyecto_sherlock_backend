from flask import Blueprint,request, jsonify
from models import User
from schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint("users", __name__)


@user_bp.get("/all")
@jwt_required()

# agregar tambien un en caso de que el usuario no tenga permisos para ver los usuarios
def get_all_users():
    """Endpoint to get all users."""
    # Paginate the users, returning 10 per page, starting from page 1
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    

    
    
    users = User.query.paginate(per_page=per_page, page=page).items
    
    results = UserSchema().dump(users,many=True)
    
    return jsonify({
        "users": results,
        
        }), 200

    