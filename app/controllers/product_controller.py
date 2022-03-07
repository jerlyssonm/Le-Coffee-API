import re
from flask import current_app, request, jsonify
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from app.models.product_model import ProductModel
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from werkzeug.exceptions import BadRequest
from app.models.region_model import RegionModel
from app.services.product_service import validate_product

def create_product():
    try:
        session: Session = current_app.db.session
        data = request.get_json()

        validated_product = validate_product(data)

        request_region = validated_product.pop("region")

        product = ProductModel(**validated_product)

        region: RegionModel = RegionModel.query.filter_by(name=request_region).first()

        product.region_id = region.id

        session.add(product)
        session.commit()

        return jsonify(product), HTTPStatus.CREATED

    except BadRequest as error:
        return error.description, error.code

    except IntegrityError as error:
        if isinstance(error.orig, UniqueViolation):
            return {"error": "Product name already exists"}, HTTPStatus.CONFLICT


def get_all_products():
    session: Session = current_app.db.session

    base_query = session.query(ProductModel)

    page = request.args.get("page", 1, type=int)

    per_page = request.args.get("per_page", 8, type=int)

    products = base_query.order_by(ProductModel.price).paginate(page, per_page)

    return jsonify(products.items), HTTPStatus.OK


def get_product_by_id(product_id):

    filtered_product: ProductModel = ProductModel.query.get(product_id)

    if not filtered_product:
        return {"msg": "Product not found"}, HTTPStatus.NOT_FOUND

    return jsonify(filtered_product), HTTPStatus.OK


def update_product(product_id):
    session: Session = current_app.db.session

    patch_product: ProductModel = ProductModel.query.get(product_id)
    data = request.get_json()

    if not patch_product:
        return {"msg": "Product not found"}, HTTPStatus.NOT_FOUND

    for keys, value in data.items():
        setattr(patch_product, keys, value)

    session.add(patch_product)
    session.commit()

    return "", HTTPStatus.OK


def delete_product(product_id):
    session: Session = current_app.db.session

    deleted_product: ProductModel = ProductModel.query.get(product_id)

    if not deleted_product:
        return {"msg": "Product not found"}, HTTPStatus.NOT_FOUND

    session.delete(deleted_product)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
