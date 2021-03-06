from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.configs.database import db


@dataclass
class FeedbackModel(db.Model):
    feedback_id: int
    text: str
    rating: int
    product_id: int
    user_id: str

    __tablename__ = "feedbacks"

    feedback_id = Column(Integer, primary_key=True)
    text = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    user = relationship("UserModel", back_populates="feedback")
    product = relationship("ProductModel", back_populates="feedbacks")