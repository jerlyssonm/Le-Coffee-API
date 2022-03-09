from http import HTTPStatus
from flask import request, jsonify
from app.configs.database import db
from sqlalchemy.orm.session import Session
from werkzeug.exceptions import NotFound
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.configs.auth import auth
from app.exception.order_exception import InvalidKeysError
from app.models.order_model import OrderModel
from app.models.product_model import ProductModel
from app.models.product_order_model import ProductsOrderModel
from app.services.order_service import check_valid_keys_order


def calc_price(cart_list: list):
    total = 0

    for item in cart_list:
        product = ProductModel.query.get_or_404(
            item["product_id"], description=f"product id {item['product_id']} not found"
        )

        price = product.price * item["quantity"]

        total = price + total

    return total


def add_item(order: OrderModel, item: dict):
    session: Session = db.session

    try:

        product = ProductModel.query.get_or_404(
            item["product_id"], description=f"product id {item['product_id']} not found"
        )

        item = ProductsOrderModel(
            quantity=item["quantity"],
            product_id=product.product_id,
            order_id=order.order_id,
        )

        order.products.append(item)

        session.commit()

    except NotFound as e:
        return {"error": f"{e.description}"}, e.code
    except AttributeError as e:
        return {"error": f"{e.description}"}, e.code


@jwt_required()
def create_order():
        session: Session = db.session

        data = request.get_json()

        valid_data = check_valid_keys_order(data)

        cart_list = valid_data.pop("cart_products")

        order = OrderModel(**valid_data)

        for item in cart_list:
            add_item(order, item)

        order.total_price = calc_price(cart_list)

        current_user = get_jwt_identity()

        order.user_id = current_user["user_id"]

        session.add(order)
        session.commit()

        return {
            "order_id": order.order_id,
            "date": order.date,
            "total_price": order.total_price,
            "user_id": order.user_id,
        }, HTTPStatus.CREATED


        

@auth.login_required
def get_all_orders():
    session: Session = db.session
    base_query = session.query(OrderModel)

    if not base_query:
        return {"orders": []}

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("perpage", 3, type=int)
    orders = base_query.order_by(OrderModel.order_id).paginate(page, per_page)

    return jsonify(orders.items), 200

@jwt_required()
def get_orders_by_user():
    session: Session = db.session

    get_jwt_user_id = get_jwt_identity()
    current_user_id = get_jwt_user_id["user_id"]

    base_query = session.query(OrderModel).filter(OrderModel.user_id == current_user_id)

    if not base_query:
        return {"orders": []}

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("perpage", 10, type=int)
    orders = base_query.order_by(OrderModel.order_id).paginate(page, per_page)

    return jsonify(orders.items), 200


@jwt_required()
def get_order_by_id(order_id: int):
    order_filtered: OrderModel = OrderModel.query.get(order_id)

    if not order_filtered:
        return {"msg": "Order not found"}, HTTPStatus.NOT_FOUND

    return jsonify(order_filtered), HTTPStatus.OK

@jwt_required()
def get_order_products(order_id: int):

    order_filtered: OrderModel = OrderModel.query.get(order_id)

    if not order_filtered:
        return {"msg": "Order not found"}, HTTPStatus.NOT_FOUND

    return jsonify(order_filtered.products), HTTPStatus.OK


@jwt_required()
def delete_order_by_id(order_id: int):
    session: Session = db.session

    deleted_order: OrderModel = OrderModel.query.get(order_id)

    if not deleted_order:
        return {"msg": "Order not found"}, HTTPStatus.NOT_FOUND

    cart = deleted_order.products

    for item in cart:
        deleted_item: ProductsOrderModel = ProductsOrderModel.query.get(
            item.product_order_id
        )
        db.session.delete(deleted_item)

    session.delete(deleted_order)
    session.commit()

    return jsonify(deleted_order), HTTPStatus.OK
