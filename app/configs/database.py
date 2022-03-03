from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.admin_model import AdminModel
    from app.models.user_model import UserModel
    # from app.models.region_model import RegionModel
    # from app.models.product_model import ProductModel
    # from app.models.order_model import OrderModel
    # from app.models.product_order_model import products_orders
    from app.models.address_model import AddressModel
    # from app.models.feedback_model import FeedbackModel

