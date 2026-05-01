from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.product import Product
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

recommendations_bp=Blueprint("recommendations",__name__)

_model=None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model=SentenceTransformer("paraphrase-MiniLM-L3-v2")
    return _model


@recommendations_bp.route("/<int:product_id>/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations(product_id):
    all_products=Product.query.all()

    if len(all_products)<2:
        return jsonify({"recommendations": []}),200

    target=next((p for p in all_products if p.id==product_id), None)
    if not target:
        return jsonify({"error": "Product not found"}),404

    model=get_model()
    texts=[f"{p.name}. {p.description}" for p in all_products]
    embeddings=model.encode(texts)

    target_index=next(i for i, p in enumerate(all_products) if p.id==product_id)
    target_embedding=embeddings[target_index].reshape(1, -1)
    similarities=cosine_similarity(target_embedding,embeddings)[0]

    scored=[
        (all_products[i],float(similarities[i]))
        for i in range(len(all_products))
        if all_products[i].id!=product_id
    ]

    scored.sort(key=lambda x: x[1],reverse=True)
    top5=scored[:5]

    recommendations=[
        {**p.to_dict(),"similarity_score": round(score, 4)}
        for p, score in top5
    ]

    return jsonify({
        "product_id": product_id,
        "recommendations": recommendations
    }),200