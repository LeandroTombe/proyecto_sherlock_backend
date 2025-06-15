from marshmallow import Schema, fields, post_load
from src.models.user import User

class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.String()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)