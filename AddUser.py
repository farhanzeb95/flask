from marshmallow import Schema, fields, validate
class User(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=15))
    created = fields.String(required=False)
