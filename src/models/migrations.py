from flask_migrate import Migrate, upgrade
from main import create_app
from extensions import db

app = create_app()

def init_db():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("Base de datos inicializada correctamente.")

def run_migrations():
    with app.app_context():
        # Ejecutar todas las migraciones pendientes
        upgrade()
        print("Migraciones aplicadas correctamente.")

if __name__ == "__main__":
    init_db()
    run_migrations() 