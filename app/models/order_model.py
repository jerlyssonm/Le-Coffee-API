from xmlrpc.client import DateTime
from app.configs.database import db
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from dataclasses import dataclass
from sqlalchemy.orm import relationship

@dataclass
class OrderModel(db.Model):
    id: int
    status: bool
    date: datetime.now()
    user_id: int

    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    status = Column(Boolean, nullable=False)
    date = Column(DateTime(), nullable=False, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="order")
    product = relationship("Product", secondary="product_order")
