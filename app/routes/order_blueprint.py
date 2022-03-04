from flask import Blueprint
from app.controllers import order_controller

bp_order = Blueprint('order', __name__, url_prefix='/orders')

bp_order.post('')(order_controller.create_order)
bp_order.get('')(order_controller.get_orders_list)
bp_order.get('/<int:order_id>')(order_controller.get_order_by_id)