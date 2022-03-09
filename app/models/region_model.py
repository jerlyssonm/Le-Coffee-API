from dataclasses import dataclass

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.configs.database import db

@dataclass
class RegionModel(db.Model):
  id: int
  name: str
  latitude: str
  longitude: str

  __tablename__ = "regions"

  id = Column(Integer, primary_key = True)
  name = Column(String, nullable = False)
  latitude = Column(String, nullable = False)
  longitude = Column(String, nullable = False)

  products = relationship("ProductModel", back_populates = "region", cascade="all, delete")