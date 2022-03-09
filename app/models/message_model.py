from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

class MessageModel(db.Model):
    messages_id: int
    text: str
    sender_id: str
    chat_id: int

    __tablename__= 'messages'

    message_id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    sender_id = Column(UUID(as_uuid=True), nullable=False)

    chat_id = Column(Integer, ForeignKey('chats.chat_id'))