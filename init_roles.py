#!/usr/bin/env python3
"""
Script para inicializar los roles básicos del sistema.
Ejecutar desde la raíz del proyecto: python init_roles.py
"""

from main import create_app
from src.config.extensions import db
from src.models.user import Role

def init_roles():
    """Inicializar los roles básicos del sistema."""
    app = create_app()
    
    with app.app_context():
        try:
            # Roles básicos del sistema
            roles = [
                {"name": "admin", "description": "Administrador del sistema"},
                {"name": "user", "description": "Usuario normal"},
                {"name": "moderator", "description": "Moderador"}
            ]
            
            for role_data in roles:
                # Verificar si el rol ya existe
                existing_role = Role.query.filter_by(name=role_data["name"]).first()
                if not existing_role:
                    role = Role(**role_data)
                    db.session.add(role)
                    print(f"✅ Rol '{role_data['name']}' creado.")
                else:
                    print(f"ℹ️  Rol '{role_data['name']}' ya existe.")
            
            db.session.commit()
            print("🎉 Roles inicializados exitosamente.")
            
        except Exception as e:
            print(f"❌ Error al inicializar roles: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == "__main__":
    init_roles()
