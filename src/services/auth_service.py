from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from src.repositories.user_repository import UserRepository
from src.models.user import User

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, data):
        # Verificar si el usuario ya existe
        if self.user_repository.get_by_username(data.get("username")):
            return {"error": "Username already exists"}, 400

        # Crear nuevo usuario
        user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password")
        )
        
        # Guardar usuario
        self.user_repository.save(user)
        
        return {"message": "User registered successfully"}, 201

    def login(self, data):
        user = self.user_repository.get_by_username(data.get("username"))
        
        if not user or not user.check_password(data.get("password")):
            return {"error": "Invalid credentials"}, 401

        # Crear tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200

    def refresh_token(self):
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        return {"access_token": access_token}, 200

    def logout(self):
        # Implementar lógica de logout si es necesario
        return {"message": "Successfully logged out"}, 200 