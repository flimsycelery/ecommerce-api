from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.review import Review
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.schemas import ReviewSchema
from marshmallow import ValidationError

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/<int:product_id>/reviews", methods=["GET"])
@jwt_required()
def get_reviews(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    reviews = Review.query.filter_by(product_id=product_id).all()
    avg = round(sum(r.rating for r in reviews) / len(reviews), 2) if reviews else 0

    return jsonify({
        "product_id":   product_id,
        "average_rating": avg,
        "total_reviews":  len(reviews),
        "reviews":      [r.to_dict() for r in reviews]
    }), 200


@reviews_bp.route("/<int:product_id>/reviews", methods=["POST"])
@jwt_required()
def add_review(product_id):
    user_id = int(get_jwt_identity())

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    ordered = db.session.query(Order).join(OrderItem).filter(
        Order.user_id == user_id,
        OrderItem.product_id == product_id
    ).first()
    if not ordered:
        return jsonify({"error": "You can only review products you have ordered"}), 403
    
    existing = Review.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return jsonify({"error": "You have already reviewed this product"}), 409

    schema = ReviewSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.messages}), 422

    review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=data["rating"],
        comment=data.get("comment")
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review added", "review": review.to_dict()}), 201


@reviews_bp.route("/<int:product_id>/reviews", methods=["DELETE"])
@jwt_required()
def delete_review(product_id):
    user_id = int(get_jwt_identity())

    review = Review.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not review:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review deleted"}), 200