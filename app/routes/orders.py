from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.extensions import db
from app.models.order import Order,OrderItem
from app.models.product import Product

orders_bp=Blueprint("orders",__name__)

@orders_bp.route("",methods=["POST"])
@jwt_required()
def place_order():
    user_id=int(get_jwt_identity())
    data=request.get_json()

    if not data or "items" not in data or not data["items"]:
        return jsonify({"error": "Order must contain atleast one item"}),422
    
    order=Order(user_id=user_id)
    db.session.add(order)

    for item in data["items"]:
        if "product_id" not in item or "quantity" not in item:
            return jsonify({"error": "Each item need product_id and quantity"}),422
        
        product=Product.query.get(item["product_id"])
        if not product:
            return jsonify({"error": f"Product {item['product_id']} no found"}),404
        
        if product.stock<item["quantity"]:
            return jsonify({"error": f"Not enough stock for {product.name}"}),400
        
        order_item=OrderItem(
            order=order,
            product=product,
            quantity=item["quantity"],
            unit_price=product.price
        )
        db.session.add(order_item)
        product.stock-=item["quantity"]

    order.calculate_total()
    db.session.commit()

    return jsonify({"message": "Order placed","order": order.to_dict()}),201

@orders_bp.route("",methods=["GET"])
@jwt_required()
def get_orders():
    user_id=int(get_jwt_identity())
    orders=Order.query.filter_by(user_id=user_id).all()
    return jsonify({"orders": [o.to_dict() for o in orders]}),200

@orders_bp.route("/<int:order_id>",methods=["GET"])
@jwt_required()
def get_order(order_id):
    user_id=int(get_jwt_identity())
    order=Order.query.filter_by(id=order_id,user_id=user_id).first()
    if not order:
        return jsonify({"error": "Order not found"}),404
    return jsonify({"order":order.to_dict()}),200