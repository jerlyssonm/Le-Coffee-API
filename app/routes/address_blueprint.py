from flask import Blueprint

from app.controllers import address_controller

bp_address = Blueprint('address', __name__, url_prefix='/address')

bp_address.post('')(address_controller.create_address)
bp_address.get('')(address_controller.get_all_addresses)
bp_address.get('/<int:address_id>')(address_controller.get_address_by_id)
bp_address.patch('/<int:address_id>')(address_controller.update_address)
bp_address.delete('/<int:address_id>')(address_controller.delete_address)