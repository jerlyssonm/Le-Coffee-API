from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.address_model import AddressModel
    from app.models.admin_model import AdminModel
    from app.models.feedback_model import FeedbackModel
    from app.models.message_model import MessageModel
    from app.models.order_model import OrderModel
    from app.models.product_model import ProductModel
    from app.models.product_order_model import ProductsOrderModel
    from app.models.region_model import RegionModel
    from app.models.user_model import UserModel