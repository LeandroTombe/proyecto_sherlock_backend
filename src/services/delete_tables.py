from main import create_app
from extensions import db
import models  # Make sure this import is present so SQLAlchemy sees your models

app = create_app()

with app.app_context():
    db.drop_all()  # Drop all existing tables
    print("Tables created successfully.")