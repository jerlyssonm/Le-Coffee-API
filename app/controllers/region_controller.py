from flask import current_app, jsonify, request

from app.models.region_model import RegionModel
from app.services.region_service import check_region_data
from app.configs.auth import auth

from sqlalchemy.exc import IntegrityError

from psycopg2.errors import NotNullViolation

from werkzeug.exceptions import NotFound

def get_regions():
  regions = RegionModel.query.all()

  return jsonify(regions), 200

@auth.login_required
def create_region():
  region_data = request.json

  try:
    region_data = check_region_data(region_data)

    new_region = RegionModel(**region_data)

    return jsonify(new_region), 

  except IntegrityError as err:
    name = region_data["name"]

    return jsonify(f"{name.title()} already exists!"), 409

  except NotNullViolation as err:
    return jsonify(err.args[0]), 400

  except TypeError as err:
    return jsonify(err.args[0]), 400

  except ValueError as err:
    return jsonify(err.args[0]), 400


@auth.login_required
def delete_region(region_id: int):
  try:
    session = current_app.db.session

    region_to_delete = RegionModel.query.get_or_404(region_id)

    session.delete(region_to_delete)
    session.commit()

  except NotFound:
    return jsonify({"msg": "region not found"}), 404

@auth.login_required
def modify_region(region_id: int):
  region_data = request.json

  try:
    session = current_app.db.session

    check_region_data(region_data)

    region = RegionModel.query.get_or_404(region_id)  

    session.add(region)
    session.commit()

    return jsonify(region), 200
  
  except NotFound:
    return jsonify({"msg": "region not found"}), 404

  except TypeError as err:
    return jsonify(err.args[0]), 400

  except ValueError as err:
    return jsonify(err.args[0]), 400