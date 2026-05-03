from app.extensions import db
from datetime import datetime, timezone


class Review(db.Model):
    __tablename__ = "reviews"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    rating     = db.Column(db.Integer, nullable=False)
    comment    = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user    = db.relationship("User", backref="reviews")
    product = db.relationship("Product", backref="reviews")

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="unique_review"),
    )

    def to_dict(self):
        return {
            "id":         self.id,
            "user":       self.user.name,
            "rating":     self.rating,
            "comment":    self.comment,
            "created_at": self.created_at.isoformat(),
        }