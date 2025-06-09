from marshmallow import Schema, fields, post_load

class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.String()

    @post_load
    def make_user(self, data, **kwargs):
        from models import User  # Import here to avoid circular import
        return User(**data)