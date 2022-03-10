from http import HTTPStatus
from itertools import product

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest, NotFound

from app.configs.database import db
from app.models.feedback_model import FeedbackModel
from app.models.product_model import ProductModel
from app.services.feedback_services import (validate_feedback,
                                            validate_feedback_update)


@jwt_required()
def create_feedback(product_id: int):
    try:
        session: Session = db.session
        data = request.get_json()
        
        validated_feedback = validate_feedback(data) 

        new_feedback = FeedbackModel(**validated_feedback)

        product: ProductModel = ProductModel.query.get(product_id)
        current_user = get_jwt_identity()

        if not product:
            return {"error_message": "Product not found"}

        new_feedback.product_id = product.product_id
        new_feedback.user_id = current_user["user_id"]

        session.add(new_feedback)
        session.commit()
        return jsonify(new_feedback), HTTPStatus.CREATED
    
    except BadRequest as error:
        return error.description, error.code


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

def get_product_feedbacks(product_id: int):
    session: Session = db.session
    base_query = session.query(FeedbackModel)

    try:
        product: ProductModel = ProductModel.query.filter_by(product_id=product_id).first_or_404(
            description="Product not found"
        )

        if not product:
            return {"error_message": "Product not found"}

        product_feedbacks = base_query.filter_by(product_id=product.product_id).all()

    except NotFound as error:
        return {"error_message": error.description}, error.code

    return jsonify(product_feedbacks), HTTPStatus.OK


def get_feedback_by_id(feedback_id: int):
    session: Session = db.session
    base_query = session.query(FeedbackModel)

    try:
        feedback = base_query.filter_by(feedback_id=feedback_id).first_or_404(
            description="Feedback not found"
        )

    except NotFound as error:
        return {"error_message": error.description}, error.code

    return jsonify(feedback), HTTPStatus.OK

@jwt_required()
def update_feedback(feedback_id: int):
    try:
        session: Session = db.session
        data = request.get_json()

        validated_update = validate_feedback_update(data)

        base_query = session.query(FeedbackModel)

        to_update = base_query.get(feedback_id)

        if not to_update:
            return {"error_message": "Feedback not found"}, HTTPStatus.NOT_FOUND

        for key, value in validated_update.items():
            setattr(to_update, key, value)

        session.add(to_update)
        session.commit()

        return jsonify(to_update), HTTPStatus.OK

    except BadRequest as error:
        return error.description, error.code

@jwt_required()
def delete_feedback(feedback_id: int):
    session: Session = db.session
    base_query = session.query(FeedbackModel)

    to_delete = base_query.get(feedback_id)

    if not to_delete:
        return jsonify({"error_message": "feedback not found"}), HTTPStatus.BAD_REQUEST

    session.delete(to_delete)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
