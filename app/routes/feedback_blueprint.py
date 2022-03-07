from flask import Blueprint
from app.controllers import feedback_controller
bp_feedback = Blueprint('feedback', __name__, url_prefix='/feedback')

bp_feedback.post('')(feedback_controller.create_record)
bp_feedback.get('')(feedback_controller.get_records)
bp_feedback.get('/<int:feedback_id>')(feedback_controller.get_record_by_id)
bp_feedback.patch('/<int:feedback_id>')(feedback_controller.update_record)
bp_feedback.delete('/<int:feedback_id>')(feedback_controller.delete_record)
