import pytest
from src.repositories.user_repository import UserRepository
from src.models.user import User, Role
from src.config.extensions import db

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
def user_repository(app):
    """Fixture que crea una instancia del repositorio de usuarios."""
    return UserRepository()

@pytest.fixture
def test_user(app):
    """Fixture que crea un usuario de prueba."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user

def test_create_user(user_repository, app):
    """Test para verificar la creación de un usuario a través del repositorio."""
    with app.app_context():
        user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        }
        
        user = user_repository.create_user(**user_data)
        
        assert user.id is not None
        assert user.username == user_data['username']
        assert user.email == user_data['email']
        assert user.check_password(user_data['password'])

def test_get_user_by_username(user_repository, app, test_user):
    """Test para verificar la búsqueda de usuario por username."""
    with app.app_context():
        found_user = user_repository.get_user_by_username('testuser')
        assert found_user is not None
        assert found_user.id == test_user.id
        
        not_found_user = user_repository.get_user_by_username('nonexistent')
        assert not_found_user is None

def test_get_user_by_id(user_repository, app, test_user):
    """Test para verificar la búsqueda de usuario por ID."""
    with app.app_context():
        found_user = user_repository.get_user_by_id(test_user.id)
        assert found_user is not None
        assert found_user.username == test_user.username
        
        not_found_user = user_repository.get_user_by_id('nonexistent-id')
        assert not_found_user is None

def test_update_user(user_repository, app, test_user):
    """Test para verificar la actualización de un usuario."""
    with app.app_context():
        update_data = {
            'email': 'updated@example.com'
        }
        
        updated_user = user_repository.update_user(test_user.id, **update_data)
        
        assert updated_user.email == update_data['email']
        assert updated_user.username == test_user.username  # No debería cambiar

def test_delete_user(user_repository, app, test_user):
    """Test para verificar la eliminación de un usuario."""
    with app.app_context():
        user_repository.delete_user(test_user.id)
        
        deleted_user = User.query.get(test_user.id)
        assert deleted_user is None

def test_get_all_users(user_repository, app):
    """Test para verificar la obtención de todos los usuarios."""
    with app.app_context():
        # Crear varios usuarios de prueba
        users = []
        for i in range(3):
            user = User(
                username=f'user{i}',
                email=f'user{i}@example.com'
            )
            user.set_password('password123')
            db.session.add(user)
            users.append(user)
        db.session.commit()
        
        all_users = user_repository.get_all_users()
        assert len(all_users) == 3
        assert all(user.username in [u.username for u in all_users] for user in users) 