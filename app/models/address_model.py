from app.configs.database import db 
from dataclasses import dataclass
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

@dataclass
class AddressModel(db.Model):
    street: str
    number: str
    city: str
    state: str
    country: str
    cep: str

    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key = True)
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Brasil")
    cep = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))

    user = relationship("UserModel", back_populates="address", cascade="all, delete")

