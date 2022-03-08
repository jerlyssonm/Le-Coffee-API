from http import HTTPStatus
from itertools import product

from flask import jsonify, request
from sqlalchemy.orm import Session
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.configs.database import db
from app.models.feedback_model import FeedbackModel
from app.models.product_model import ProductModel


@jwt_required()
def create_feedback(product_id: int):
    data = request.get_json()

    session: Session = db.session

    new_feedback = FeedbackModel(**data)

    product: ProductModel = ProductModel.query.get(product_id)
    current_user = get_jwt_identity()

    if not product:
        return {"error_message": "Product not found"}

    new_feedback.product_id = product.product_id
    new_feedback.user_id = current_user["user_id"]

    session.add(new_feedback)
    session.commit()

    return jsonify(new_feedback), HTTPStatus.CREATED


def get_all_feedbacks():
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
        feedbacks = base_query.filter(**query_params).order_by(FeedbackModel.feedback_id)
    else:
        feedbacks = base_query.order_by(FeedbackModel.feedback_id)

    feedbacks = feedbacks.paginate(page, per_page)

    return jsonify(feedbacks.items), HTTPStatus.OK


def get_feedback_by_id(feedback_id: int):
    session: Session = db.session
    base_query = session.query(FeedbackModel)

    try:
        feedback = base_query.filter_by(feedback_id=feedback_id).first_or_404(
            description="feedback not found"
        )

    except NotFound as error:
        return {"error_message": error.description}, error.code

    return jsonify(feedback), HTTPStatus.OK

@jwt_required()
def update_feedback(feedback_id: int):
    data = request.get_json()

    session: Session = db.session

    base_query = session.query(FeedbackModel)

    to_update = base_query.get(feedback_id)

    if not to_update:
        return {"error": "feedback not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(to_update, key, value)

    session.add(to_update)
    session.commit()

    return jsonify(to_update), HTTPStatus.OK

@jwt_required()
def delete_feedback(feedback_id: int):
    session: Session = db.session
    base_query = session.query(FeedbackModel)

    to_delete = base_query.get(feedback_id)

    if not to_delete:
        return jsonify({"error": "feedback not found"}), HTTPStatus.BAD_REQUEST

    session.delete(to_delete)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
