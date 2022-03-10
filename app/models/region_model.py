from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.configs.database import db
from app.models.product_model import ProductModel


@dataclass
class RegionModel(db.Model):
  id: int
  name: str
  latitude: str
  longitude: str
  products: ProductModel

  __tablename__ = "regions"

  id = Column(Integer, primary_key = True)
  name = Column(String, nullable = False)
  latitude = Column(String, nullable = False)
  longitude = Column(String, nullable = False)

  products = relationship("ProductModel", back_populates = "region",  cascade="all, delete")