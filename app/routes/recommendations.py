from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models.product import Product
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

recommendations_bp = Blueprint("recommendations", __name__)

_cache = {
    "embeddings": None,
    "product_ids": None,
    "vectorizer": None
}


def build_cache(products):
    """Build and store TF-IDF embeddings for all products."""
    texts = [f"{p.name}. {p.description}" for p in products]
    vectorizer = TfidfVectorizer(stop_words="english")
    embeddings = vectorizer.fit_transform(texts)

    _cache["embeddings"] = embeddings
    _cache["product_ids"] = [p.id for p in products]
    _cache["vectorizer"] = vectorizer


def invalidate_cache():
    """Call this when products are added or deleted."""
    _cache["embeddings"] = None
    _cache["product_ids"] = None
    _cache["vectorizer"] = None


@recommendations_bp.route("/<int:product_id>/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations(product_id):
    all_products = Product.query.all()

    if len(all_products) < 2:
        return jsonify({"recommendations": []}), 200

    target = next((p for p in all_products if p.id == product_id), None)
    if not target:
        return jsonify({"error": "Product not found"}), 404

    if _cache["embeddings"] is None:
        build_cache(all_products)

    embeddings = _cache["embeddings"]
    product_ids = _cache["product_ids"]

    target_index = product_ids.index(product_id)
    similarities = cosine_similarity(embeddings[target_index], embeddings)[0]

    scored = [
        (all_products[i], float(similarities[i]))
        for i in range(len(all_products))
        if all_products[i].id != product_id
    ]

    scored.sort(key=lambda x: x[1], reverse=True)
    top5 = scored[:5]

    recommendations = [
        {**p.to_dict(), "similarity_score": round(score, 4)}
        for p, score in top5
    ]

    return jsonify({
        "product_id": product_id,
        "recommendations": recommendations
    }), 200