from flask import Blueprint,request, jsonify
from src.models.user import User, Role
from src.api.schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.decorators import role_required

user_bp = Blueprint("users", __name__)


@user_bp.get("/all")
@jwt_required()
@role_required(["admin"])  # Solo administradores pueden ver todos los usuarios
def get_all_users():
    """Endpoint to get all users."""
    # Paginate the users, returning 10 per page, starting from page 1
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    

    
    
    users = User.query.paginate(per_page=per_page, page=page).items
    
    results = UserSchema().dump(users,many=True)
    
    return jsonify({
        "users": results,
        "page": page,
        "per_page": per_page
    }), 200

@user_bp.post("/<user_id>/roles")
@jwt_required()
@role_required(["admin"])
def add_role_to_user(user_id):
    """Agregar un rol a un usuario."""
    data = request.get_json()
    role_name = data.get('role')
    
    if not role_name:
        return jsonify({"error": "El nombre del rol es requerido"}), 400
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
        
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"error": "Rol no encontrado"}), 404
        
    user.add_role(role)
    user.save()
    
    return jsonify({
        "message": f"Rol {role_name} agregado al usuario {user.username}",
        "user_roles": [role.name for role in user.roles]
    }), 200

@user_bp.delete("/<user_id>/roles")
@jwt_required()
@role_required(["admin"])
def remove_role_from_user(user_id):
    """Remover un rol de un usuario."""
    data = request.get_json()
    role_name = data.get('role')
    
    if not role_name:
        return jsonify({"error": "El nombre del rol es requerido"}), 400
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
        
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"error": "Rol no encontrado"}), 404
        
    user.remove_role(role)
    user.save()
    
    return jsonify({
        "message": f"Rol {role_name} removido del usuario {user.username}",
        "user_roles": [role.name for role in user.roles]
    }), 200

    