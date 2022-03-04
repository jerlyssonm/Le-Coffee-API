from email.mime import base
from http import HTTPStatus

from flask import jsonify, request
from sqlalchemy import JSON
from sqlalchemy.orm import Session

from app.configs.database import db
from app.models.address_model import AddressModel


def create_record():
    data = request.get_json()
    session: Session = db.session

    record = AddressModel(**data)
    session.add(record)
    session.commit()

    return jsonify(record), HTTPStatus.CREATED


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


def delete_record(address_id: int):
    session: Session = db.session
    base_query = session.query(AddressModel)

    record = base_query.get(address_id)

    if not record:
        return jsonify({"error": "address not found"}), HTTPStatus.BAD_REQUEST
    
    session.delete(record)
    session.commit()
    
    return "", HTTPStatus.NO_CONTENT

def update_record(address_id: int):
    data = request.get_json()

    session: Session = db.session

    base_query = session.query(AddressModel)

    record = base_query.get(address_id)

    if not record:
        return {"error": "Address not found"}, HTTPStatus.NOT_FOUND
    
    for key, value in data.items():
        setattr(record, key, value)
    
    session.add(record)
    session.commit()

    return jsonify(record), HTTPStatus.OK
