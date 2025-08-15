import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from main import create_app
from src.config.extensions import db
from src.models.user import User, Role, TokenBlocklist  # Importar modelos para que SQLAlchemy los vea

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created successfully.")