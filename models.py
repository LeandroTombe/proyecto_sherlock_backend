from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

def generate_uuid():
    """Generate a unique identifier."""
    return str(uuid4())


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True, default=(generate_uuid))
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500))

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()