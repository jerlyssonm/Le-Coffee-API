from app.models.order_model import OrderModel
from http import HTTPStatus

def get_order_by_id(order_id):
    order : OrderModel = Order.query.get(order_id)

    return jsonify(order), HTTPStatus.OK

