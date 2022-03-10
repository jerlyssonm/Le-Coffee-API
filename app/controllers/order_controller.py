from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from werkzeug.exceptions import BadRequest, NotFound

from app.configs.auth import auth
from app.configs.database import db
from app.models.order_model import OrderModel
from app.models.product_model import ProductModel
from app.models.product_order_model import ProductsOrderModel
from app.services.order_service import check_valid_keys_order


def calc_price(cart_list: list):
    total = 0

    for cart_product in cart_list:
        product: ProductModel = ProductModel.query.get_or_404(
            cart_product["product_id"],
            description={
                "error_message": f"Product with id {cart_product['product_id']} not found"
            },
        )

        price = product.price * cart_product["quantity"]

        total = price + total

    return total


def add_item(order: OrderModel, cart_product: dict):
    session: Session = db.session

    product: ProductModel = ProductModel.query.get_or_404(
        cart_product["product_id"],
        description={
            "error_message": f"Product with id {cart_product['product_id']} not found"
        },
    )

    cart_product = ProductsOrderModel(
        quantity=cart_product["quantity"],
        product_id=product.product_id,
        order_id=order.order_id,
    )

    order.products.append(cart_product)

    session.commit()


@jwt_required()
def create_order():
    try:
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

    except BadRequest as error:
        return error.description, error.code

    except NotFound as error:
        return error.description, error.code

    except IntegrityError as error:
        if isinstance(error.orig, ForeignKeyViolation):
            return { "error_message": "User not found for this autentication"  }


@auth.login_required
def get_all_orders():
    session: Session = db.session
    base_query = session.query(OrderModel)

    if not base_query:
        return {"orders": []}

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("perpage", 5, type=int)
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

    return jsonify(orders.items), HTTPStatus.OK


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
