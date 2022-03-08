from app.models.order_model import OrderModel
from http import HTTPStatus
from flask import request, jsonify
from app.configs.database import db
from sqlalchemy.orm.session import Session
from werkzeug.exceptions import NotFound
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.product_model import ProductModel
from app.models.product_order_model import ProductsOrderModel

""" def create_order():
    data = request.get_json()
    order = OrderModel(**data)

    db.session.add(order)
    db.session.commit()

    return jsonify(order), HTTPStatus.CREATED

def add_item(order_id: int):
    data = request.get_json()

    try:
        product_id = data['product_id']
        quantity = data['quantity']

        order = OrderModel.query.get_or_404(order_id, description=f'order id {order_id} not found')
        product = ProductModel.query.get_or_404(product_id, description=f'product id {product_id} not found')

        order.products.append(order.product)

        db.session.commit()

        return jsonify({"msg" : "ok"}), 200

    except KeyError as e:
        return {"error": f"missing key {e.args[0]}"}, HTTPStatus.BAD_REQUEST

    except NotFound as e:

        return {"error": f"order id {e.args[0]}"}, HTTPStatus.NOT_FOUND """

def add_item(order: OrderModel, item: dict):

    try:
        
        product = ProductModel.query.get_or_404(
            item['id'], description=f"product id {item['id']} not found"
        )
        
        item = ProductsOrderModel(quantity = item['quantity'],product_id = product.product_id, order_id=order.order_id)

        order.products.append(item)

        db.session.commit()

    except NotFound as e:
        return {"error": f"{e.description}"}, e.code

@jwt_required()
def create_order():
    data = request.get_json()
    final_price = 0
    cart_list = data.pop("cart_products")
        
    order = OrderModel(**data)

    for item in cart_list:
        add_item(order, item) 

    """ order.total_price = calc_price(cart_list) """

    current_user = get_jwt_identity()
    
    order.user_id = current_user

    db.session.add(order)
    db.session.commit()

    return {
        "order_id": order.order_id,
        "date": order.date,
        "total_price": """ order.total_price """ ,
        "user_id": order.user_id,
    }



def get_all_orders():
    session: Session = db.session
    base_query = session.query(OrderModel)

    if not base_query:
        return {"orders": []}

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("perpage", 3, type=int)
    orders = base_query.order_by(OrderModel.order_id).paginate(page, per_page)

    return jsonify(orders.items), 200

def get_order_by_id(order_id):
    order_filtered: OrderModel = OrderModel.query.get(order_id)

    if not order_filtered:
        return {"msg": "Order not found"}, HTTPStatus.NOT_FOUND

    return jsonify(order_filtered), HTTPStatus.OK

def get_order_products(order_id: int):

    order_filtered: OrderModel = OrderModel.query.get(order_id)

    if not order_filtered:
        return {"msg": f"Order {order_id} not found"}, HTTPStatus.NOT_FOUND
    
    return jsonify(order_filtered.products), HTTPStatus.OK


def delete_order_by_id(order_id):
    deleted_order: OrderModel = OrderModel.query.get(order_id)

    if not deleted_order:
        return {"msg": "Order not found" }, HTTPStatus.NOT_FOUND

    db.session.delete(deleted_order)
    db.session.commit()

    return jsonify(deleted_order), HTTPStatus.OK