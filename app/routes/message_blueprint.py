from flask import Blueprint
from app.controllers import message_controller

bp_order = Blueprint('message', __name__, url_prefix='/messages')

bp_order.post('')(message_controller.create_message)
bp_order.get('')(message_controller.get_all_messages)
bp_order.get('/chat/<int:chat_id>')(message_controller.get_message_by_chat)
bp_order.patch('')(message_controller.update_message)
bp_order.delete('<int:message_id>')(message_controller.delete_message)