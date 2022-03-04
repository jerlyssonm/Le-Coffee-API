from flask import Blueprint
from app.controllers import order_controller
bp_order = Blueprint('order', __name__, url_prefix='/orders')

bp_admin.post('/register')(admin_controller.signup)
bp_admin.post('/login')(admin_controller.signin)
# bp_admin.patch('')(admin_controller.update_admin)
# bp_admin.delete('')(admin_controller.delete_admin)

