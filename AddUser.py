from marshmallow import Schema, fields, validate
class User(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=15))
    created = fields.String(required=False)

class AddItem(Schema):
    name= fields.String(requires=True)
    description= fields.String(required=True)
    condition= fields.String(required=True)
    price= fields.String(required=True)
    category= fields.String(required=True)
    dateAdded= fields.String(required=False)
    status= fields.String(required=False)
    email=fields.Email(required=True)
    image=fields.String(required=True)
