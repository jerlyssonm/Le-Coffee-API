from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session
from http import HTTPStatus
from werkzeug.exceptions import NotFound

from app.configs.database import db
from app.models.message_model import MessageModel

@jwt_required()
def create_message():
    session: Session = db.session
    data = request.get_json

    current_user = get_jwt_identity()

    message = MessageModel(**data)
    message.sender_id = current_user
    session.add(message)
    session.commit()

    return jsonify(message), HTTPStatus.CREATED

def get_all_message():
    session: Session = db.session
    try:
        message_by_chat = session.query(MessageModel)
    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    return jsonify(message_by_chat), HTTPStatus.OK

def get_message_by_chat(chat_id):
    session: Session = db.session
    try:
        message_by_chat = session.query(MessageModel).filter_by(chat_id=chat_id)
    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    return jsonify(message_by_chat), HTTPStatus.OK


def update_message():
    ...

def delete_message():
    session: Session = db.session
    try:
        message_by_chat = session.query(MessageModel).filter_by(chat_id=chat_id)
    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
    
    for item in message_by_chat:
        session.delete(item)
    ...