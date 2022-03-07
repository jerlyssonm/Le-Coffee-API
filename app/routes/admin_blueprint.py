from flask import Blueprint
from app.controllers import admin_controller
bp_admin = Blueprint('admin', __name__, url_prefix='/admin')

bp_admin.post('/register')(admin_controller.signup)
bp_admin.post('/login')(admin_controller.signin)
bp_admin.get('')(admin_controller.get_all_admin)
# bp_admin.get('<int:admin_id>')(admin_controller.get_admin_by_id)
bp_admin.patch('')(admin_controller.update_admin)
bp_admin.delete('')(admin_controller.delete_admin)