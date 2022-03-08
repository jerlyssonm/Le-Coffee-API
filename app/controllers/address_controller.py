from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import JSON
from sqlalchemy.orm import Session
from werkzeug.exceptions import NotFound, BadRequest

from app.configs.database import db
from app.models.address_model import AddressModel
from app.models.user_model import UserModel
from app.services.address_service import check_address_data


@jwt_required()
def create_record():
    session: Session = db.session
    data = request.get_json()
    user_on = get_jwt_identity()

    try:
        validated_data = check_address_data(data)

        user: UserModel = UserModel.query.filter_by(email=user_on["email"]).first()

        record = AddressModel(**validated_data)

        record.user_id = user.user_id

        session.add(record)
        session.commit()

    except BadRequest as error:
        return {"error": error.description}

    return jsonify(record), HTTPStatus.CREATED


@jwt_required()
def get_records():
    session: Session = db.session
    base_query = session.query(AddressModel)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    source = request.args.get("source", type=int)
    destination = request.args.get("destination")

    query_params = dict(request.args)
    query_params.pop("page", None)
    query_params.pop("per_page", None)

    if source or destination:
        records = base_query.filter(**query_params).order_by(AddressModel.address_id)
    else:
        records = base_query.order_by(AddressModel.address_id)
    
    records = records.paginate(page, per_page)

    return jsonify(records.items), HTTPStatus.OK


@jwt_required()
def get_record_by_id(address_id: int):
    session: Session = db.session
    base_query = session.query(AddressModel)

    try: 
        record = base_query.filter_by(address_id=address_id).first_or_404(description="address not found")
    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
    
    return jsonify(record), HTTPStatus.OK


@jwt_required()
def delete_record(address_id: int):
    session: Session = db.session
    base_query = session.query(AddressModel)

    record = base_query.get(address_id)

    if not record:
        return jsonify({"error": "address not found"}), HTTPStatus.BAD_REQUEST
    
    session.delete(record)
    session.commit()
    
    return "", HTTPStatus.NO_CONTENT


@jwt_required()
def update_record(address_id: int):
    session: Session = db.session

    data = request.get_json()

    base_query = session.query(AddressModel)

    record = base_query.get(address_id)

    if not record:
        return {"error": "Address not found"}, HTTPStatus.NOT_FOUND
    
    for key, value in data.items():
        setattr(record, key, value)
    
    session.add(record)
    session.commit()

    return jsonify(record), HTTPStatus.OK
