from flask import Blueprint
from app.controllers import address_controller
bp_address = Blueprint('address', __name__, url_prefix='/address')

bp_address.post('')(address_controller.create_record)
bp_address.get('')(address_controller.get_records)
bp_address.patch('')(address_controller.update_record)
bp_address.delete('')(address_controller.delete_record)