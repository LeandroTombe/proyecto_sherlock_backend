from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)
from models import User, TokenBlocklist, Role
from extensions import db
from datetime import datetime, UTC

auth_bp = Blueprint("auth", __name__)



@auth_bp.post("/register")
def register_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user is not None:
        return jsonify({"error": "El usuario ya existe"}), 409

    new_user = User(
        username=data.get("username"), 
        email=data.get("email")
    )

    new_user.set_password(password=data.get("password"))
    
    # Asignar rol 'user' por defecto
    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        # Si el rol no existe, crearlo
        user_role = Role(name='user', description='Usuario normal')
        db.session.add(user_role)
        db.session.commit()
    
    new_user.roles.append(user_role)
    new_user.save()

    return jsonify({
        "message": "Usuario creado",
        "roles": [role.name for role in new_user.roles]
    }), 201


@auth_bp.post("/login")
def login_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user is None or not user.check_password(password=data.get("password")):
        return jsonify({"error": "el usuario o contraseña son invalidos"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "message": "Inicio de sesión exitoso",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200
    
@auth_bp.get("/whoami")
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "message",
            "user_details": {
                "username": current_user.username,
                "email": current_user.email,
                "roles": [role.name for role in current_user.roles]
            },
        }
    )


@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    
    access_token = create_access_token(identity=identity)
    
    return jsonify({"access_token": access_token}), 200
    

@auth_bp.delete("/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(UTC)
    
    db.session.add(TokenBlocklist(jti=jti, user_id=current_user.id))
    db.session.commit()
    
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200
    
    
