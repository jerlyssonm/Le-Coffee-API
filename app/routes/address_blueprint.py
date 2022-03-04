from flask import Blueprint
from app.controllers import address_controller
bp_products = Blueprint('address', __name__, url_prefix='/address')

bp_products.post('')(address_controller.create_record)
bp_products.get('')(address_controller.get_records)
bp_products.patch('')(address_controller.update_record)
bp_products.delete('')(address_controller.delete_record)