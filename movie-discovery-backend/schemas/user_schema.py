# schemas/user_schema.py
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    password = fields.String(required=True, load_only=True)
    is_admin = fields.Boolean(default=False)  # Field to specify if the user is an admin
