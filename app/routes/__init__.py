from flask import Flask

from app.routes.admin_blueprint import bp_admin
from app.routes.product_blueprint import bp_products
from app.routes.user_blueprint import bp_user
from app.routes.region_blueprint import bp_region
from app.routes.address_blueprint import bp_address
from app.routes.order_blueprint import bp_order

def init_app(app: Flask):
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_products)
    app.register_blueprint(bp_region)
    app.register_blueprint(bp_address) 
    app.register_blueprint(bp_order)
