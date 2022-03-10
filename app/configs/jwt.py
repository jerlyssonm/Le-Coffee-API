from os import getenv
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager


def init_app(app: Flask):
    app.config["JWT_SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
 
    JWTManager(app)