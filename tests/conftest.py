import pytest
from flask import Flask
from src.config.extensions import db
from src.models.user import User, Role

@pytest.fixture
def app():
    """Fixture que crea una aplicación Flask para pruebas."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Fixture que crea un cliente de prueba."""
    return app.test_client()

@pytest.fixture
def user_role(app):
    """Fixture que crea un rol de usuario para pruebas."""
    with app.app_context():
        role = Role(name='user', description='Usuario normal')
        db.session.add(role)
        db.session.commit()
        return role

@pytest.fixture
def admin_role(app):
    """Fixture que crea un rol de administrador para pruebas."""
    with app.app_context():
        role = Role(name='admin', description='Administrador')
        db.session.add(role)
        db.session.commit()
        return role

@pytest.fixture
def test_user(app, user_role):
    """Fixture que crea un usuario de prueba."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        user.roles.append(user_role)
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def admin_user(app, admin_role):
    """Fixture que crea un usuario administrador de prueba."""
    with app.app_context():
        user = User(
            username='admin',
            email='admin@example.com'
        )
        user.set_password('admin123')
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
        return user 