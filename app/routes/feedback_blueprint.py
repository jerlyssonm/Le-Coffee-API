from flask import Blueprint

from app.controllers import feedback_controller

bp_feedback = Blueprint('feedback', __name__, url_prefix='/feedbacks')

bp_feedback.post('/<int:product_id>')(feedback_controller.create_feedback)
bp_feedback.get('')(feedback_controller.get_all_feedbacks)
bp_feedback.get('/product/<int:product_id>')(feedback_controller.get_product_feedbacks)
bp_feedback.get('/<int:feedback_id>')(feedback_controller.get_feedback_by_id)
bp_feedback.patch('/<int:feedback_id>')(feedback_controller.update_feedback)
bp_feedback.delete('/<int:feedback_id>')(feedback_controller.delete_feedback)
