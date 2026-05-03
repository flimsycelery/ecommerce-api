from app.extensions import db
from datetime import datetime, timezone


class Wishlist(db.Model):
    __tablename__ = "wishlists"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user    = db.relationship("User", backref="wishlist_items")
    product = db.relationship("Product", backref="wishlisted_by")

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="unique_wishlist_item"),
    )

    def to_dict(self):
        return {
            "id":         self.id,
            "product":    self.product.to_dict(),
            "added_at":   self.created_at.isoformat(),
        }