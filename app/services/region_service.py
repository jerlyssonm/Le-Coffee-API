import re
from os import getenv

from flask import current_app
from werkzeug.exceptions import BadRequest

from app.models.region_model import RegionModel


def check_data_to_create_region(request_data: dict):

    valid_keys = set(getenv("REGION_KEYS").split(","))
    valid_regions = getenv("REGIONS").split(",")
    allowed_number_of_keys_ = 3
   
    if len(request_data) < allowed_number_of_keys_:
        missing_keys = valid_keys - set(request_data.keys())
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}

        raise BadRequest(description=error_description)

    wrong_keys = set(request_data.keys()) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )

    
    wrong_values_type = [value for value in request_data.values() if type(value) != str]

    if wrong_values_type:
        raise BadRequest(
            description={"error_message": "All field values must be a string type"}
        )

    if request_data["name"] not in valid_regions:
        raise BadRequest(
            description={
                "available_regions": valid_regions,
                "wrong_region": request_data["name"],
            }
        )

    latitude: str = request_data["latitude"]
    match_rule_latitude = r"^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$"
    match_response_latitude = re.fullmatch(match_rule_latitude, latitude)

    if match_response_latitude is None:
        raise BadRequest(
            description={
                "error_message": "latitude is invalid",
                "valid_latitude": {"max_value": "+90.000000", "min_value": "-90.000000"},
                "invalid_latitude": latitude,
            }
        )

    longitude: str = request_data["longitude"]
    match_rule_longitude = r"^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$"
    match_response_longitude = re.fullmatch(match_rule_longitude, longitude)

    if match_response_longitude is None:
        raise BadRequest(
            description={
                "error_message": "longitude is invalid",
                "valid_longitude": {"max_value": "+180.000000", "min_value": "-180.000000"},
                "invalid_longitude": longitude,
            }
        )

    if "name" in request_data.keys():
        name: str = request_data["name"]
        request_data["name"] = name.title()

    return request_data
    

def check_data_to_update_region(data: dict):

    valid_keys = set(getenv("REGION_KEYS").split(","))
    valid_regions = getenv("REGIONS").split(",")

    wrong_keys = set(data.keys()) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )

    wrong_values_type = [value for value in data.values() if type(value) != str]

    if wrong_values_type:
        raise BadRequest(
            description={"error_message": "All field values must be a string type"}
        )

    if "name" in data.keys():
        name: str = data["name"]
        if name not in valid_regions:
            raise BadRequest({
                "available_regions": valid_regions,
                "wrong_region": name
            })

        data["name"] = name.title()

    latitude: str = data.get("latitude")
    if latitude:
        match_rule_latitude = (
            r"^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$"
        )
        match_response_latitude = re.fullmatch(match_rule_latitude, latitude)

        if match_response_latitude is None:
            raise BadRequest(
                description={
                    "error_message": "latitude is invalid",
                    "valid_latitude": {"max_value": "+90.000000", "min_value": "-90.000000"},
                    "invalid_latitude": latitude,
                }
            )

    longitude: str = data.get("longitude")
    if longitude:
        match_rule_longitude = r"^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$"
        match_response_longitude = re.fullmatch(match_rule_longitude, longitude)

        if match_response_longitude is None:
            raise BadRequest(
                description={
                    "error_message": "longitude is invalid",
                    "valid_longitude": {"max_value": "+180.000000", "min_value": "-180.000000"},
                    "invalid_longitude": longitude,
                }
            )

    return data


def region_populate():
    if not RegionModel.query.all():

        region_coordinates = [
        { "name": "Norte", "latitude": "-4.19802", "longitude": "-64.3398" },
        { "name": "Nordeste", "latitude": "-5.86494", "longitude":"-40.57466"},
        { "name": "Centro-Oeste", "latitude": "-16.71819","longitude": "-53.29242" },
        { "name": "Sudeste", "latitude": "-21.03781", "longitude":"-45.71101" },
        { "name": "Sul", "latitude": "-27.29441", "longitude":"-51.41195"}
        ]

        for data in region_coordinates:
            region: RegionModel = RegionModel(**data)
            current_app.db.session.add(region)
        current_app.db.session.commit()
