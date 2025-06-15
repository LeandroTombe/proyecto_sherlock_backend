from src.models.user import User
from src.config.extensions import db

class UserRepository:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_by_id(self, user_id):
        return User.query.get(user_id)

    def save(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user):
        db.session.commit()
        return user

    def delete(self, user):
        db.session.delete(user)
        db.session.commit() 