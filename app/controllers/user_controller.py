from http import HTTPStatus
from flask import jsonify, request,current_app
from sqlalchemy.exc import IntegrityError

from flask_jwt_extended import  create_access_token  

from app.services.register_service import validate_request
from app.models.user_model import UserModel  

from werkzeug.exceptions import NotFound


def signup():
    session = current_app.db.session
    
    data = request.get_json()

    validate_data = validate_request(data)

    password_to_hash = validate_data.pop("password")

    try:
        new_user: UserModel = UserModel(**validate_data)
        new_user.password = password_to_hash

        session.add(new_user)
        session.commit()

        return jsonify(new_user), HTTPStatus.CREATED

    except IntegrityError:
        return {"msg":"email already exists"}, HTTPStatus.CONFLICT

def signin():
    data = request.get_json

    user: UserModel = UserModel.query.filter_by(email=data["email"]).first()

    if not user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND
    
    if not user:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    user.verify_password(data["password"])
    access_token = create_access_token(identity=user)
    user["token"] = access_token
    return jsonify(user), HTTPStatus.OK
    
def get_user_all():

    all_users = UserModel.query.all()

    return jsonify(all_users), HTTPStatus.OK

def get_user_by_email(email):

    try:
        user = UserModel.query.filter_by(email=email).first()

        return jsonify(user),HTTPStatus.OK
        
    except NotFound:
        return {"message": "Product NotFound"},HTTPStatus.NOT_FOUND
     