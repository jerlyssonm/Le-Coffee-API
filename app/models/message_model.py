from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.configs.database import db


@dataclass
class MessageModel(db.Model):
    message_id: int
    text: str
    user_id: str
    order_id: int

    __tablename__= 'messages'

    message_id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    order_id: int = Column(Integer, ForeignKey("orders.order_id"))

    order = relationship("OrderModel", back_populates = "message")
    user = relationship("UserModel", back_populates = "message")