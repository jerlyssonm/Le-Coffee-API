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
    data = request.get_json()

    current_user = get_jwt_identity()
    message = MessageModel(**data)
    message.sender_id = current_user["user_id"]
    session.add(message)
    session.commit()

    return jsonify(message), HTTPStatus.CREATED

def get_message_by_chat(chat_id: int):
    session: Session = db.session
    base_query = session.query(MessageModel)

    try:
        message = MessageModel.query.filter_by(chat_id=chat_id).first()

        if not message:
            raise NotFound

    except NotFound as error:
        return {"error": "Messages not found in database."}, error.code
    
    message_filtrer = base_query.filter_by(chat_id=chat_id).all()
    
    return jsonify(message_filtrer), HTTPStatus.OK

def get_message_by_id(message_id: int):
    session: Session = db.session
    base_query = session.query(MessageModel)

    message = base_query.get(message_id)

    if not message:
            return {"error": "Message not found in database."}, HTTPStatus.NOT_FOUND

    return jsonify(message), HTTPStatus.OK

@jwt_required()
def update_message(message_id: int):
    session: Session = db.session
    data = request.get_json()
    base_query = session.query(MessageModel)
    current_user = get_jwt_identity()

    message_to_update = base_query.get(message_id)
    print(message_to_update.sender_id)

    #if message_to_update.sender_id != current_user['user_id'] :
    #    return {"error": "Unauthorized Access."}, HTTPStatus.NOT_FOUND

    if not message_to_update:
        return {"error": "Message not found in database."}, HTTPStatus.NOT_FOUND
    
    for key, value in data.items():
        setattr(message_to_update, key, value)

    session.add(message_to_update)
    session.commit()

    return jsonify(message_to_update), HTTPStatus.OK

@jwt_required()
def delete_message(message_id: int):
    session: Session = db.session
    base_query = session.query(MessageModel)

    message = base_query.get(message_id)

    if not message:
        return {"error": "Message not found in database."}, HTTPStatus.NOT_FOUND
    
    session.delete(message)
    session.commit()

    return jsonify(message), HTTPStatus.OK