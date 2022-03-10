from os import getenv
from werkzeug.exceptions import BadRequest
import re

def validate_product(request_data: dict):
    valid_keys = set(getenv("PRODUCT_KEYS").split(","))
    valid_categories = getenv("CATEGORY_TYPES").split(",")
    valid_regions = getenv("REGIONS").split(",")

    allowed_number_of_keys_ = 7

    if len(request_data) < allowed_number_of_keys_:
        missing_keys = valid_keys - set(request_data.keys())
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}

        raise BadRequest(description=error_description)

    wrong_keys = set(request_data) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )

    if request_data['category'] not in valid_categories:
        error_description = {"Invalid Category": request_data['category'], "Categories availiable": valid_categories}

        raise BadRequest(description=error_description)

    request_data['region'] = request_data['region'].title()
    
    if request_data['region'] not in valid_regions:
        error_description = {"Invalid Region": request_data['region'], "regions availiable": valid_regions}
    

        raise BadRequest(description=error_description)

    latitude: str = request_data["latitude"]
    match_rule_latitude = r"^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$"
    match_response_latitude = re.fullmatch(match_rule_latitude, latitude)

    if match_response_latitude is None:
        raise BadRequest({
            "error_message": "latitude is invalid",
            "valid_latitude": {
            "max_value": "+90.000",
            "min_value": "-90.00"
            },
            "invalid_latitude": latitude
        })

    longitude: str = request_data["longitude"]
    match_rule_longitude = r"^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$"
    match_response_longitude = re.fullmatch(match_rule_longitude, longitude)
    
    if match_response_longitude is None:
        raise BadRequest({
            "error_message": "longitude is invalid",
            "valid_longitude": {
                "max_value": "+180.000",
                "min_value": "-180.000"
            },
            "invalid_longitude": longitude
        })


    formatted_data = {
        'name': request_data['name'].title().strip(),
        'price': float('{:.2f}'.format(request_data['price'])) ,
        'description': request_data['description'],
        'region': request_data['region'],
        'category': request_data['category'],
        'latitude': request_data['latitude'],
        'longitude': request_data['longitude'],
    }


    return formatted_data


def validate_product_update(request_data: dict):
    valid_keys = set(getenv("PRODUCT_KEYS").split(","))
    wrong_keys = set(request_data) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )
    
    if 'name' in request_data.keys():
        request_data['name'] = request_data['name'].title()
    
    return request_data