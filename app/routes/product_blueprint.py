from flask import Blueprint
from app.controllers import product_controller
bp_products = Blueprint('products', __name__, url_prefix='/products')

bp_products.post('')(product_controller.create_product)
bp_products.get('')(product_controller.get_all_products)
bp_products.get('')(product_controller.get_product_by_id)
bp_products.patch('')(product_controller.update_product)
bp_products.delete('')(product_controller.delete_product_by_id)