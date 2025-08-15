import pytest
from src.models.user import User, Role
from src.config.extensions import db
from datetime import datetime, UTC

@pytest.fixture
def app():
    """Fixture que crea una aplicación Flask para pruebas."""
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user_role(app):
    """Fixture que crea un rol de usuario para pruebas."""
    with app.app_context():
        role = Role(name='user', description='Usuario normal')
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

def test_create_user(app):
    """Test para verificar la creación de un usuario."""
    with app.app_context():
        user = User(
            username='newuser',
            email='new@example.com'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'newuser'
        assert user.email == 'new@example.com'
        assert user.password is not None

def test_password_hashing(app):
    """Test para verificar el hashing de contraseñas."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        
        assert user.check_password('password123') is True
        assert user.check_password('wrongpassword') is False

def test_user_roles(app, test_user, user_role):
    """Test para verificar la asignación de roles."""
    with app.app_context():
        assert len(test_user.roles) == 1
        assert test_user.has_role('user') is True
        assert test_user.has_role('admin') is False

def test_add_remove_role(app, test_user):
    """Test para verificar la adición y eliminación de roles."""
    with app.app_context():
        admin_role = Role(name='admin', description='Administrador')
        db.session.add(admin_role)
        db.session.commit()
        
        test_user.add_role(admin_role)
        assert test_user.has_role('admin') is True
        
        test_user.remove_role(admin_role)
        assert test_user.has_role('admin') is False

def test_get_user_by_username(app, test_user):
    """Test para verificar la búsqueda de usuario por username."""
    with app.app_context():
        found_user = User.get_user_by_username('testuser')
        assert found_user is not None
        assert found_user.id == test_user.id
        
        not_found_user = User.get_user_by_username('nonexistent')
        assert not_found_user is None

def test_user_save_delete(app):
    """Test para verificar el guardado y eliminación de usuarios."""
    with app.app_context():
        user = User(
            username='tempuser',
            email='temp@example.com'
        )
        user.set_password('password123')
        user.save()
        
        saved_user = User.query.filter_by(username='tempuser').first()
        assert saved_user is not None
        
        saved_user.delete()
        deleted_user = User.query.filter_by(username='tempuser').first()
        assert deleted_user is None 