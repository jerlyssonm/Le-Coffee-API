from app.configs.database import db 
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class AdminModel(db.Model):
    id: int
    name: str
    email: str

    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=True)
    adm_key = db.Column(db.String, nullable=False)


    @property
    def password(self):
        raise AttributeError("Password cannot be acessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)