from flask import jsonify

from app.models.chat_model import ChatModel
from app.models.order_model import OrderModel
from app.configs.database import db

from werkzeug.exceptions import NotFound

session = db.session

def create_chat(order_id):
  try: 
    OrderModel.query.get_or_404(order_id)

    data = {
      "order_id": order_id
    }

    new_chat = ChatModel(**data)

    session.add(new_chat)
    session.commit()

    return jsonify(new_chat), 201

  except NotFound:
    return jsonify({"msg": "order not found"}), 404

def get_chat(chat_id):
  try:
    chat = ChatModel.query.get_or_404(chat_id)

    return jsonify(chat), 200

  except NotFound:
    return jsonify({"msg": "chat not found"}), 404