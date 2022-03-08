from flask import Blueprint
from app.controllers import user_controller


bp_user = Blueprint("users",__name__, url_prefix="/users")

bp_user.post("/register")(user_controller.signup)
bp_user.post("/login")(user_controller.signin)
bp_user.get("")(user_controller.get_user_all)
bp_user.get("/getone")(user_controller.get_one_user)
bp_user.put("")(user_controller.update_user)
bp_user.delete("")(user_controller.delete_user)
