from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ForeignKeyViolation

from app.configs.database import db
from app.models.message_model import MessageModel
from app.services.message_services import validate_message


@jwt_required()
def create_message(order_id: int):
    try:
        session: Session = db.session
        data = request.get_json()
        data["order_id"] = order_id
        print(data)
        validate_message(data)

        current_user = get_jwt_identity()
        message = MessageModel(**data)
        message.user_id = current_user["user_id"]
        session.add(message)
        session.commit()

        return jsonify(message), HTTPStatus.CREATED

    except BadRequest as error:
        return error.description, error.code

    except IntegrityError as error:
        if isinstance(error.orig, ForeignKeyViolation):
            return { "msg": "Order not found in database"  }

def get_message_by_order(order_id: int):
    session: Session = db.session
    base_query = session.query(MessageModel)

    try:
        message = MessageModel.query.filter_by(order_id=order_id).first()

        if not message:
            raise NotFound

    except NotFound as error:
        return {"msg": "Messages not found in database"}, error.code
    
    message_filtrer = base_query.filter_by(order_id=order_id).all()
    
    return jsonify(message_filtrer), HTTPStatus.OK

def get_message_by_id(message_id: int):
    session: Session = db.session
    base_query = session.query(MessageModel)

    message = base_query.get(message_id)

    if not message:
            return {"msg": "Message not found in database"}, HTTPStatus.NOT_FOUND

    return jsonify(message), HTTPStatus.OK