from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.configs.database import db


@dataclass
class ProductModel(db.Model):
    name: str
    price: float
    # image: str
    description: str
    category: str

    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    # image =  Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    category = Column(String)
    latitude = Column(String)
    longitude = Column(String)

    region_id = Column(Integer, ForeignKey("regions.id"))

    region = relationship("RegionModel", back_populates="products", uselist=False)
    feedbacks = relationship("FeedbackModel", back_populates="product", cascade="all, delete")