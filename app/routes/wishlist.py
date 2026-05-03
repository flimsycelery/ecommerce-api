from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.wishlist import Wishlist
from app.models.product import Product

wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("", methods=["GET"])
@jwt_required()
def get_wishlist():
    user_id = int(get_jwt_identity())
    items = Wishlist.query.filter_by(user_id=user_id).all()
    return jsonify({
        "wishlist": [item.to_dict() for item in items],
        "total": len(items)
    }), 200


@wishlist_bp.route("/<int:product_id>", methods=["POST"])
@jwt_required()
def add_to_wishlist(product_id):
    user_id = int(get_jwt_identity())

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    existing = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return jsonify({"error": "Product already in wishlist"}), 409

    item = Wishlist(user_id=user_id, product_id=product_id)
    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Added to wishlist", "item": item.to_dict()}), 201


@wishlist_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_wishlist(product_id):
    user_id = int(get_jwt_identity())

    item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        return jsonify({"error": "Product not in wishlist"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Removed from wishlist"}), 200