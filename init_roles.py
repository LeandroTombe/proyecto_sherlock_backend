from main import create_app
from extensions import db
from models import Role, User

def init_roles():
    app = create_app()
    with app.app_context():
        try:
            # Crear roles básicos
            roles = [
                Role(name='admin', description='Administrador del sistema'),
                Role(name='user', description='Usuario normal'),
                Role(name='moderator', description='Moderador del sistema')
            ]
            
            # Agregar roles a la base de datos
            for role in roles:
                existing_role = Role.query.filter_by(name=role.name).first()
                if not existing_role:
                    print(f"Creando rol: {role.name}")
                    db.session.add(role)
                else:
                    print(f"Rol ya existe: {role.name}")
            
            db.session.commit()
            print("Roles inicializados correctamente.")
            
            # Verificar roles creados
            all_roles = Role.query.all()
            print("\nRoles en la base de datos:")
            for role in all_roles:
                print(f"- {role.name}: {role.description}")
                
        except Exception as e:
            print(f"Error al inicializar roles: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    init_roles() 