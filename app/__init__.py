from flask import Flask,jsonify
from app.config import get_config
from app.extensions import db,migrate,jwt

def create_app():
    app=Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

    from app.models import user,product,order

    @app.route("/health")
    def health():
        return jsonify({"status":"ok"}),200
    return app