from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String

class MessageModel(db.Model):
    messages_id: int
    text: str
    sender_id: int
    chat_id: int

    __tablename__= 'messages'

    message_id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    sender_id = Column(Integer, nullable=False)

    chat_id = Column(Integer, ForeignKey('chat.chat_id'))