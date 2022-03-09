from xmlrpc.client import DateTime
from app.configs.database import db
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

@dataclass
class OrderModel(db.Model):
    order_id: int
    status: bool
    date: datetime.now()
    user_id: int

    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    status = Column(Boolean, nullable=False)
    date = Column(DateTime(), nullable=False, default=datetime.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    user = relationship("UserModel", back_populates="order", cascade="all, delete")
    products = relationship("ProductsOrderModel" , cascade="all, delete")
    chat = relationship("ChatModel", cascade="all, delete")