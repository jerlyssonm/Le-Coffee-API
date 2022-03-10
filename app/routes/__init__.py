from flask import Flask

from app.routes.address_blueprint import bp_address
from app.routes.admin_blueprint import bp_admin
from app.routes.feedback_blueprint import bp_feedback
from app.routes.message_blueprint import bp_message
from app.routes.order_blueprint import bp_order
from app.routes.product_blueprint import bp_products
from app.routes.region_blueprint import bp_region
from app.routes.user_blueprint import bp_user


def init_app(app: Flask):
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_products)
    app.register_blueprint(bp_region)
    app.register_blueprint(bp_address) 
    app.register_blueprint(bp_order)
    app.register_blueprint(bp_feedback)
    app.register_blueprint(bp_message)
