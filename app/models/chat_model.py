from app.configs.database import db

from dataclasses import dataclass

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

@dataclass
class ChatModel(db.Model):
  chat_id: int
  order_id: int

  __tablename__ = "chats"

  chat_id: int = Column(Integer, primary_key = True)
  order_id: int = Column(Integer, ForeignKey("orders.order_id"))

  order = relationship("OrderModel", back_populates = "chat")