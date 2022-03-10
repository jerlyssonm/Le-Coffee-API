from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.configs.database import db


@dataclass
class UserModel(db.Model):
    user_id: str
    name: str
    email: str

    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=True)

    address = relationship("AddressModel", back_populates="user", cascade="all, delete")
    feedback = relationship("FeedbackModel", back_populates="user", cascade="all, delete")
    order = relationship("OrderModel", back_populates="user", cascade="all, delete")

    @property
    def password(self):
        raise AttributeError("Password cannot be acessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
    
