from flask import current_app, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

from app.configs.auth import auth
from app.models.region_model import RegionModel
from app.services.region_service import (check_data_to_create_region,
                                         check_data_to_update_region)


def get_regions():
    regions = RegionModel.query.all()

    return jsonify(regions), 200
    

@auth.login_required
def create_region():
    region_data = request.get_json()

    try:
        session = current_app.db.session

        region_data = check_data_to_create_region(region_data)

        new_region = RegionModel(**region_data)

        session.add(new_region)
        session.commit()

        return jsonify(new_region), 201

    except BadRequest as err:
        return err.description, err.code


@auth.login_required
def update_region(region_id: int):
    region_data = request.get_json()

    try:
        session = current_app.db.session

        region_data = check_data_to_update_region(region_data)

        region = RegionModel.query.get_or_404(region_id)

        for key, value in region_data.items():
            setattr(region, key, value)

        session.add(region)
        session.commit()

        return jsonify(region), 200

    except NotFound:
        return jsonify({"msg": "region not found"}), 404

    except BadRequest as err:
        return err.description, err.code

@auth.login_required
def delete_region(region_id: int):
    try:
        session = current_app.db.session

        region_to_delete = RegionModel.query.get_or_404(region_id)

        session.delete(region_to_delete)
        session.commit()

        return jsonify(), 204

    except NotFound:
        return jsonify({"msg": "region not found"}), 404
