from flask import Blueprint
from app.controllers import user_controller


bp_user = Blueprint("users",__name__, url_prefix="/user")

bp_user.post("/register")(user_controller.signup)
bp_user.post("/login")(user_controller.signin)
bp_user.get("")(user_controller.get_product_all)
bp_user.get("/<int:id>")(user_controller.get_product_by_id)