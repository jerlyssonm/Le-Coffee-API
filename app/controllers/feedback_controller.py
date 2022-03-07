from http import HTTPStatus

from flask import jsonify, request
from sqlalchemy.orm import Session
from werkzeug.exceptions import NotFound

from app.configs.database import db
from app.models.feedback_model import FeedbackModel


def create_record():
    data = request.get_json()
    session: Session = db.session

    record = FeedbackModel(**data)
    session.add(record)
    session.commit()

    return jsonify(record), HTTPStatus.CREATED


def get_records():
    session: Session = db.session
    base_query = session.query(FeedbackModel)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    source = request.args.get("source", type=int)
    destination = request.args.get("destination")

    query_params = dict(request.args)
    query_params.pop("page", None)
    query_params.pop("per_page", None)

    if source or destination:
        records = base_query.filter(**query_params).order_by(FeedbackModel.feedback_id)
    else:
        records = base_query.order_by(FeedbackModel.feedback_id)
    
    records = records.paginate(page, per_page)

    return jsonify(records.items), HTTPStatus.OK


def get_record_by_id(feedback_id: int):
    session: Session = db.session
    base_query = session.query(FeedbackModel)

    try: 
        record = base_query.filter_by(feedback_id=feedback_id).first_or404(description="feedback not found")
    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
    
    return jsonify(record), HTTPStatus.OK


def delete_record(feedback_id: int):
    session: Session = db.session
    base_query = session.query(FeedbackModel)

    record = base_query.get(feedback_id)

    if not record:
        return jsonify({"error": "feedback not found"}), HTTPStatus.BAD_REQUEST
    
    session.delete(record)
    session.commit()
    
    return "", HTTPStatus.NO_CONTENT


def update_record(feedback_id: int):
    data = request.get_json()

    session: Session = db.session

    base_query = session.query(FeedbackModel)

    record = base_query.get(feedback_id)

    if not record:
        return {"error": "feedback not found"}, HTTPStatus.NOT_FOUND
    
    for key, value in data.items():
        setattr(record, key, value)
    
    session.add(record)
    session.commit()

    return jsonify(record), HTTPStatus.OK