from flask_httpauth import HTTPTokenAuth
from app.models.admin_model import AdminModel

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(api_key: str):
    user = AdminModel.query.filter_by(api_key=api_key).first()

    return user
    