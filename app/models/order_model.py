from dataclasses import dataclass
from datetime import datetime
from xmlrpc.client import DateTime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.configs.database import db
from app.models.product_model import ProductModel


@dataclass
class OrderModel(db.Model):
    order_id: int
    status: bool
    date: datetime.now()
    products: ProductModel

    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    status = Column(Boolean, nullable=False)
    date = Column(DateTime(), nullable=False, default=datetime.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    user = relationship("UserModel", back_populates="order")
    products = relationship("ProductsOrderModel")
    message = relationship("MessageModel", cascade="all, delete")