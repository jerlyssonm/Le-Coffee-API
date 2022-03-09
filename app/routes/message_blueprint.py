from flask import Blueprint
from app.controllers import message_controller

bp_message = Blueprint('message', __name__, url_prefix='/messages')

bp_message.post('')(message_controller.create_message)
bp_message.get('/<int:message_id>')(message_controller.get_message_by_id)
bp_message.get('/order/<int:order_id>')(message_controller.get_message_by_order)
bp_message.patch('/<int:message_id>')(message_controller.update_message)
bp_message.delete('<int:message_id>')(message_controller.delete_message)