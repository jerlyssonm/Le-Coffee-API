from app.configs.database import db 
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer
from uuid import uuid4


@dataclass
class AdminModel(db.Model):
    id: str
    name: str
    email: str

    __tablename__ = "admin"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=True)
    adm_key = Column(String, nullable=False)


    @property
    def password(self):
        raise AttributeError("Password cannot be acessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)