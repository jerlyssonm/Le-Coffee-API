from os import getenv

from flask import Flask
from flask_jwt_extended import JWTManager


def init_app(app: Flask):
    app.config["JWT_SECRET_KEY"] = getenv("SECRET_KEY")
 
    JWTManager(app)