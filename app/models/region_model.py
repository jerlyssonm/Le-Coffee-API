from dataclasses import dataclass
from app.configs.database import db

@dataclass
class RegionModel(db.Model):
  id: int
  name: str
  latitude: str
  longitude: str

  __tablename__ = "region"

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String, nullable = False)
  latitude = db.Column(db.String, nullable = False)
  longitude = db.Column(db.String, nullable = False)