from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.extensions import db
from app.models.product import Product
from app.utils.auth_helpers import admin_required

products_bp=Blueprint("products",__name__)

@products_bp.route("",methods=["GET"])
@jwt_required()
def get_products():
    category=request.args.get("category")
    min_price=request.args.get("min_price", type=float)
    max_price=request.args.get("max_price", type=float)
    page=request.args.get("page", 1, type=int)
    per_page=request.args.get("per_page", 10, type=int)

    query=Product.query

    if category:
        query=query.filter_by(category=category)
    if min_price is not None:
        query=query.filter(Product.price >= min_price)
    if max_price is not None:
        query=query.filter(Product.price <= max_price)

    paginated=query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "products": [p.to_dict() for p in paginated.items],
        "pagination": {
            "page": paginated.page,
            "per_page": paginated.per_page,
            "total": paginated.total,
            "pages": paginated.pages,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev
        }
    }),200

@products_bp.route("/<int:product_id>",methods=["GET"])
@jwt_required()
def get_product(product_id):
    product=Product.query.get_or_404(product_id)
    return jsonify({"product":product.to_dict()}),200

@products_bp.route("",methods=["POST"])
@admin_required
def create_product():
    data=request.get_json()
    if not data or not all(k in data for k in ("name","description","price","stock","category")):
        return jsonify({"error":"All fields are required"}),422
    
    product=Product(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        stock=data["stock"],
        category=data["category"]
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product created","product":product.to_dict()}),201