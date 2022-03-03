from enum import unique
from app.configs.database import db 
from dataclasses import dataclass

@dataclass
class UserModel(db.Model):
    user_id: int
    name: str
    email: str
    password: str

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    
    
