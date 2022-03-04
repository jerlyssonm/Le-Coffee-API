from flask import Flask

from app.routes.admin_blueprint import bp_admin
from app.routes.product_blueprint import bp_products

def init_app(app: Flask):
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_products)