from src.config.extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC

def generate_uuid():
    """Generate a unique identifier."""
    return str(uuid4())

# Tabla de asociación para roles de usuario
user_roles = db.Table('user_roles',
    db.Column('user_id', db.String, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.String, db.ForeignKey('roles.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500))
    roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                          backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def add_role(self, role):
        if not self.has_role(role.name):
            self.roles.append(role)

    def remove_role(self, role):
        if self.has_role(role.name):
            self.roles.remove(role)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<TokenBlocklist {self.jti}>'