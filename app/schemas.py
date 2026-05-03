from marshmallow import Schema, fields, validate, ValidationError


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class ProductSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=10))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    stock = fields.Int(required=True, validate=validate.Range(min=0))
    category = fields.Str(required=True, validate=validate.Length(min=2, max=100))


class OrderItemSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))


class OrderSchema(Schema):
    items = fields.List(fields.Nested(OrderItemSchema), required=True, validate=validate.Length(min=1))

class ReviewSchema(Schema):
    rating  = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=False, validate=validate.Length(max=500))