from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.product import Product
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

recommendations_bp=Blueprint("recommendations", __name__)


@recommendations_bp.route("/<int:product_id>/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations(product_id):
    all_products=Product.query.all()

    if len(all_products)<2:
        return jsonify({"recommendations": []}), 200

    target=next((p for p in all_products if p.id == product_id), None)
    if not target:
        return jsonify({"error": "Product not found"}), 404

    texts=[f"{p.name}. {p.description}" for p in all_products]

    vectorizer=TfidfVectorizer(stop_words="english")
    tfidf_matrix=vectorizer.fit_transform(texts)

    target_index=next(i for i, p in enumerate(all_products) if p.id==product_id)

    similarities=cosine_similarity(tfidf_matrix[target_index], tfidf_matrix)[0]

    scored=[
        (all_products[i], float(similarities[i]))
        for i in range(len(all_products))
        if all_products[i].id!=product_id
    ]

    scored.sort(key=lambda x: x[1], reverse=True)
    top5=scored[:5]

    recommendations=[
        {**p.to_dict(), "similarity_score": round(score, 4)}
        for p, score in top5
    ]

    return jsonify({
        "product_id": product_id,
        "recommendations": recommendations
    }), 200