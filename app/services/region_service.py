from psycopg2.errors import NotNullViolation
import re
from os import getenv
from werkzeug.exceptions import BadRequest


def check_region_data(data: dict):

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

    if data["name"] not in valid_regions:
        raise BadRequest(
            description={
                "available_regions": valid_regions,
                "wrong_region": data["name"],
            }
        )

    latitude: str = data["latitude"]
    match_rule_latitude = (
        r"^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$"
    )
    match_response_latitude = re.fullmatch(match_rule_latitude, latitude)

    if match_response_latitude is None:
        raise BadRequest(
            description={
                "error_message": "latitude is invalid",
                "valid_latitude": {"max_value": "+90.000", "min_value": "-90.00"},
                "invalid_latitude": latitude,
            }
        )

    longitude: str = data["longitude"]
    match_rule_longitude = r"^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$"
    match_response_longitude = re.fullmatch(match_rule_longitude, longitude)

    if match_response_longitude is None:
        raise BadRequest(
            description={
                "error_message": "longitude is invalid",
                "valid_longitude": {"max_value": "+180.000", "min_value": "-180.000"},
                "invalid_longitude": longitude,
            }
        )

    if "name" in data.keys():
        name: str = data["name"]
        data["name"] = name.title()

    return data
