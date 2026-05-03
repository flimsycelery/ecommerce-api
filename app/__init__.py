from flask import Flask, jsonify
from app.config import get_config
from app.extensions import db, migrate, jwt, limiter


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or get_config())

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    from app.models import user, product, order

    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.orders import orders_bp
    from app.routes.admin import admin_bp
    from app.routes.recommendations import recommendations_bp
    from app.routes.wishlist import wishlist_bp
    from app.routes.reviews import reviews_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(recommendations_bp, url_prefix="/products")
    app.register_blueprint(wishlist_bp, url_prefix="/wishlist")
    app.register_blueprint(reviews_bp, url_prefix="/products")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return jsonify({"error": "Too many requests. Try again in a minute"}), 429

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app