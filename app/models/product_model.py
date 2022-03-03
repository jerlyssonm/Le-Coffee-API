from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text

from sqlalchemy.orm import relationship
from app.configs.database import db

@dataclass
class ProductModel(db.Model):
    name: str
    price: float
    category: str
    description: str

    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    price = Column(Float, primary_key=True)
    category = Column(String, primary_key=True)
    description = Column(Text, primary_key=True)
    latitude = Column(String, primary_key=True)
    longitude = Column(String, primary_key=True)

    region_id = Column(Integer, ForeignKey("regions.id"))

    region = relationship("RegionModel", back_populates="products", uselist=False)