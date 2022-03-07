from secrets import token_urlsafe
from flask import current_app, request, jsonify
from http import HTTPStatus
from app.models.admin_model import AdminModel
from app.configs.auth import auth
from app.services.register_login_service import validate_request
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError

def signup():
    try:
        session = current_app.db.session

        admin_data = request.get_json()

        validate_data = validate_request(admin_data)

        validate_data['adm_key'] = token_urlsafe(16)

        password_to_hash = validate_data.pop("password")

        new_admin = AdminModel(**validate_data)

        new_admin.password = password_to_hash


        session.add(new_admin)
        session.commit()

        return jsonify(new_admin), HTTPStatus.CREATED

    except IntegrityError:
        return {"error": "Admin already exists"}, HTTPStatus.CONFLICT

def signin():
    admin_data =  request.get_json()

    validate_login = validate_request(admin_data, type_login=True)
    
    admin: AdminModel = AdminModel.query.filter_by(email = validate_login['email']).first()

    if not admin:
        return {"error": "email not found"}, HTTPStatus.UNAUTHORIZED
    
    if not admin.verify_password(validate_login['password']):
        return {"error": "email and password missmatch"}, HTTPStatus.UNAUTHORIZED


    return jsonify({"admin_key": admin.adm_key}), HTTPStatus.OK


@auth.login_required
def get_all_admin():   
    admins: AdminModel = AdminModel.query.all()
    return jsonify(admins), HTTPStatus.OK
    

@auth.login_required
def delete_admin():
    session = current_app.db.session
    admin = auth.current_user()
    
    session.delete(admin)
    session.commit()

    return {"msg": f"Admin {admin.name} has been deleted."}, HTTPStatus.OK

@auth.login_required
def update_admin(): 
    session = current_app.db.session
    data = request.get_json()
    admin = auth.current_user()

    if "password" in data: 
        password_to_hash = data.pop("password")
        admin.password = password_to_hash
    
    for key, value in data.items():
        setattr(admin, key, value)

    session.add(admin)
    session.commit()

    return jsonify(admin), HTTPStatus.OK