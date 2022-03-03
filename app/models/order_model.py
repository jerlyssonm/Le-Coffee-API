from app.configs.database import db
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from dataclasses import dataclass

@dataclass
class OrderModel(db.Model):
    id: int
    status: Boolean
    date: datetime
    user_id: int

    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    status = Column(Boolean)
    date = Column(datetime)
    user_id = Column(Integer, ForeignKey("users.id"))

    estados = db.relationship("EstadoModel", backref="regiao")