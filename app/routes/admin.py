from flask import Blueprint,request,jsonify
from app.extensions import db
from app.models.order import Order
from app.models.product import Product
from app.utils.auth_helpers import admin_required

admin_bp=Blueprint("admin",__name__)

VALID_STATUSES=["pending","confirmed","shipped","delivered","cancelled"]

@admin_bp.route("/orders",methods=["GET"])
@admin_required
def get_all_orders():
    status=request.args.get("status")
    query=Order.query
    if status:
        query=query.filter_by(status=status)
    orders=query.order_by(Order.created_at.desc()).all()
    return jsonify({"orders":[o.to_dict() for o in orders]}),200

@admin_bp.route("/orders/<int:order_id>/status",methods=["PATCH"])
@admin_required
def update_order_status(order_id):
    order=Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data=request.get_json()
    if not data or "status" not in data:
        return jsonify({"error": "Status is required"}), 422

    if data["status"] not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Must be one of {VALID_STATUSES}"}), 422

    order.status=data["status"]
    db.session.commit()

    return jsonify({"message": "Order status updated", "order": order.to_dict()}), 200


@admin_bp.route("/products/<int:product_id>", methods=["DELETE"])
@admin_required
def delete_product(product_id):
    product=Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": f"Product {product.name} deleted"}), 200
